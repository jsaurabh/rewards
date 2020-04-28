from rest_framework import serializers

from drp.catalog import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        exclude = ()


class CategoryItemSerializer(CategorySerializer):
    items = ItemSerializer(many=True)
