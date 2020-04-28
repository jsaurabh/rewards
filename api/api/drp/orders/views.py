from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from drp.orders import models, serializers
from drp.programs.models import Business
from drp.rewards.utils import process_order


User = get_user_model()


class OrderView(generics.CreateAPIView):
    serializer_class = serializers.CreateOrderSerializer
    queryset = models.Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        business = serializer.validated_data["business"]
        customer = serializer.validated_data["customer"]
        line_items = serializer.validated_data["line_items"]

        with transaction.atomic():
            order = models.Order.objects.create(
                business=business, customer=customer, employee=request.user,
            )

            for line_item in line_items:
                item = line_item["menu_item"]
                quantity = line_item["quantity"]
                models.LineItem.objects.create(
                    order=order, menu_item=item, quantity=quantity,
                )

            order.refresh_from_db()

            process_order(order)

        return Response(serializers.OrderSerializer(order).data)
