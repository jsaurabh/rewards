from django.contrib.auth import get_user_model
from rest_framework import serializers

from drp.programs.models import Business
from drp.programs.serializers import CurrencySerializer
from drp.rewards.models import AccumulationRule, RedemptionRule


User = get_user_model()


class AccumulationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccumulationRule
        exclude = ()

    def validate(self, data):
        campaign = data["campaign"]
        category = data["category"]
        item = data["item"]

        if category and item:
            raise serializers.ValidationError(
                "Only one of category and item can be provided per accumulation rule."
            )

        if category and category.business != campaign.business:
            raise serializers.ValidationError(
                "The category does not belong to the business running the campaign."
            )

        if item and item.category.business != campaign.business:
            raise serializers.ValidationError(
                "The item does not belong to the business running the campaign."
            )

        return data


class RedemptionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedemptionRule
        exclude = ()


class AccumulatedPointsSerializer(serializers.Serializer):
    currency = CurrencySerializer()
    accumulated = serializers.IntegerField()
    rewards = RedemptionRuleSerializer(many=True)


class _RewardSerialzier(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    rule = serializers.PrimaryKeyRelatedField(queryset=RedemptionRule.objects.all())


class RedeemRewardSerializer(serializers.Serializer):
    business = serializers.PrimaryKeyRelatedField(queryset=Business.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    rewards = _RewardSerialzier(many=True, allow_empty=False)

    def validate(self, data):
        business = data["business"]
        customer = data["customer"]
        rewards = data["rewards"]

        if not business.customers.filter(id=customer.id).exists():
            raise serializers.ValidationError(
                "Customer is not enrolled in this rewards program."
            )

        for reward in rewards:
            if reward["rule"].campaign.business != business:
                raise serializers.ValidationError(
                    "Redemption rule is not from this business."
                )

        return data
