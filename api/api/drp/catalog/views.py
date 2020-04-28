from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets

from drp.catalog import serializers
from drp.catalog.models import Category, Item
from drp.programs.models import Business


class BusinessCatalogView(generics.ListAPIView):
    serializer_class = serializers.CategoryItemSerializer

    def get_queryset(self):
        business_id = self.kwargs["business_id"]
        business = get_object_or_404(Business, id=business_id)
        user = self.request.user
        if not business.employees.filter(id=user.id).exists():
            raise PermissionDenied
        return Category.objects.filter(business=business)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(business__employees=user)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(category__business__employees=user)
