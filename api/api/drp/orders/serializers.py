from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from drp.catalog.models import Item
from drp.orders import models
from drp.programs.models import Business


User = get_user_model()


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LineItem
        exclude = ("order",)


class OrderSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True)

    class Meta:
        model = models.Order
        exclude = ()
        read_only_fields = (
            "created_at",
            "employee",
        )


class CreateOrderSerializer(serializers.Serializer):
    business = serializers.PrimaryKeyRelatedField(
        queryset=Business.objects.filter(is_published=True)
    )
    customer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True)
    )
    line_items = LineItemSerializer(many=True, allow_empty=False)

    def validate(self, data):
        business = data["business"]
        customer = data["customer"]
        line_items = data["line_items"]

        request = self.context["request"]
        if not business.employees.filter(id=request.user.id).exists():
            print(request.user, business.employees.all())
            raise PermissionDenied("You are not an employee of the specified business.")

        if not business.customers.filter(id=customer.id).exists():
            raise serializers.ValidationError(
                "Customer is not enrolled in this rewards program."
            )

        if any(li["quantity"] <= 0 for li in line_items):
            raise serializers.ValidationError("All quantities should be positive.")

        item_ids = [li["menu_item"].id for li in line_items]
        menu_items = Item.objects.filter(id__in=item_ids)
        incorrect_menu_items = menu_items.exclude(category__business=business)
        if incorrect_menu_items.exists():
            raise serializers.ValidationError(
                "All menu items are not from this business."
            )

        return data
