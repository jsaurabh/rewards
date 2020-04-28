from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drp.programs import models, serializers
from drp.users.serializers import CustomerSerializer, UserSerializer


class BusinessEmployeeFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(business__employees=user)


class BusinessViewSet(ModelViewSet):
    queryset = models.Business.objects.all()
    serializer_class = serializers.BusinessSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_published=True)
            only_where_not_customer = "not-customer" in self.request.query_params
            if only_where_not_customer:
                queryset = queryset.exclude(id__in=self.request.user.customer_of.all())
        elif self.action != "retrieve":
            queryset = queryset.filter(employees=self.request.user)
        return queryset

    def perform_create(self, serializer):
        business = serializer.save()
        business.employees.add(self.request.user)
        currency = models.Currency.objects.create(business=business, label="Points")
        models.Campaign.objects.create(
            name="{} rewards".format(business.name),
            business=business,
            currency=currency,
        )

    @action(detail=True)
    def employees(self, request, pk=None):
        return Response(self._serialize_employees())

    @employees.mapping.post
    def add_employee(self, request, pk=None):
        business = self.get_object()
        user = self._get_employee()
        business.employees.add(user)
        return Response(self._serialize_employees())

    @employees.mapping.delete
    def remove_employee(self, request, pk=None):
        business = self.get_object()
        user = self._get_employee()
        business.employees.remove(user)
        return Response(self._serialize_employees())

    def _serialize_employees(self):
        business = self.get_object()
        employees = business.employees.all()
        return UserSerializer(employees, many=True).data

    def _get_employee(self):
        serializer = serializers.EmployeeSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["user"]


class CampaignViewSet(BusinessEmployeeFilterMixin, ModelViewSet):
    queryset = models.Campaign.objects.all()
    serializer_class = serializers.CampaignSerializer


class CurrencyViewSet(BusinessEmployeeFilterMixin, ModelViewSet):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class JoinProgramView(APIView):
    def post(self, request, business_id):
        business = get_object_or_404(models.Business, id=business_id)
        business.customers.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeaveProgramView(APIView):
    def post(self, request, business_id):
        business = get_object_or_404(models.Business, id=business_id)
        business.customers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerListView(ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        business = get_object_or_404(models.Business, id=self.kwargs["business_id"])
        queryset = business.customers
        user_id = self.request.query_params.get("id")
        if user_id:
            queryset = queryset.filter(id=user_id)
        phone = self.request.query_params.get("phone")
        if phone:
            queryset = queryset.filter(phone=phone)
        return queryset
