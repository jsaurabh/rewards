from django.contrib.auth import get_user_model
from rest_framework import serializers

from drp.programs import models


User = get_user_model()


class CurrencySerializer(serializers.ModelSerializer):
    # TODO: singular_label and plural_label are only here for
    # backwards-compatibility, and should be removed once they
    # are no longer being used.
    singular_label = serializers.CharField(source="label", read_only=True)
    plural_label = serializers.CharField(source="label", read_only=True)

    class Meta:
        model = models.Currency
        exclude = ()


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Business
        exclude = ("customers", "employees")


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Campaign
        exclude = ()

    def validate(self, data):
        business = data["business"]
        currency = data["currency"]

        if business != currency.business:
            raise serializers.ValidationError(
                "Currency does not belong to this business."
            )

        return data


class EmployeeSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True)
    )
