from collections import defaultdict
import heapq

from django.db import transaction
from django.db.models import Count, F
from django.db.models.expressions import Star, Value
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drp.programs.models import Business, Currency
from drp.programs.utils import get_active_campaigns
from drp.rewards.models import AccumulationRule, Point, Redemption, RedemptionRule
from drp.rewards.serializers import (
    AccumulationRuleSerializer,
    AccumulatedPointsSerializer,
    RedeemRewardSerializer,
    RedemptionRuleSerializer,
)
from drp.rewards.utils import get_points_for_user


_business_param = openapi.Parameter(
    "business",
    openapi.IN_QUERY,
    description="A unique integer value identifying a business.",
    required=True,
    type=openapi.TYPE_INTEGER,
)
_customer_param = openapi.Parameter(
    "customer",
    openapi.IN_QUERY,
    description="A unique integer value identifying a user.",
    required=True,
    type=openapi.TYPE_INTEGER,
)
_currency_param = openapi.Parameter(
    "currency",
    openapi.IN_QUERY,
    description="A unique integer value identifying a currency.",
    required=True,
    type=openapi.TYPE_INTEGER,
)


class AccumulationRuleViewSet(ModelViewSet):
    queryset = AccumulationRule.objects.all()
    serializer_class = AccumulationRuleSerializer


class RedemptionRuleViewSet(ModelViewSet):
    queryset = RedemptionRule.objects.all()
    serializer_class = RedemptionRuleSerializer


class RedeemView(APIView):
    @swagger_auto_schema(manual_parameters=[_business_param, _customer_param])
    def get(self, request):
        business_id = self.request.query_params.get("business")
        customer_id = self.request.query_params.get("customer")
        business = get_object_or_404(Business, id=business_id)
        customer = get_object_or_404(business.customers, id=customer_id)
        campaigns = get_active_campaigns(business.campaigns)
        currencies_by_id = {
            currency.id: currency
            for currency in Currency.objects.filter(business=business)
        }
        redemption_rules = RedemptionRule.objects.filter(campaign__in=campaigns)
        redemption_rules_by_currency = defaultdict(list)
        for rule in redemption_rules:
            currency = rule.campaign.currency
            redemption_rules_by_currency[currency.id].append(rule)
        points = get_points_for_user(customer, business)

        summary = {
            currency_id: {
                "currency": currencies_by_id[currency_id],
                "accumulated": points_accumulated,
                "rewards": redemption_rules_by_currency[currency_id],
            }
            for currency_id, points_accumulated in points.items()
        }
        for currency in currencies_by_id.values():
            if currency.id not in summary:
                summary[currency.id] = {
                    "currency": currency,
                    "accumulated": 0,
                    "rewards": redemption_rules_by_currency[currency.id],
                }

        return Response(AccumulatedPointsSerializer(summary.values(), many=True).data)

    @swagger_auto_schema(
        request_body=RedeemRewardSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: "Success",
            status.HTTP_400_BAD_REQUEST: "Failure",
        },
    )
    def post(self, request):
        serializer = RedeemRewardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        business = serializer.validated_data["business"]
        customer = serializer.validated_data["customer"]
        rewards = serializer.validated_data["rewards"]

        try:
            with transaction.atomic():
                for reward in rewards:
                    quantity = reward["quantity"]
                    rule = reward["rule"]
                    value = rule.value
                    currency = rule.campaign.currency

                    currency_points_needed = quantity * value

                    points = (
                        Point.objects.select_for_update()
                        .redeemable(currency=currency, customer=customer)
                        .order_by(F("expires_at").asc(nulls_last=True))[
                            :currency_points_needed
                        ]
                    )
                    if points.count() != currency_points_needed:
                        raise ValueError(
                            "Insufficient points for currency {} "
                            "when redeeming rule {}.".format(currency.id, rule.id)
                        )

                    for i, point in enumerate(points):
                        new_redemption = i % value == 0
                        if new_redemption:
                            redemption = Redemption.objects.create(
                                user=customer,
                                currency=currency,
                                value=value,
                                reward=rule.reward,
                            )
                        point.redemption = redemption
                    Point.objects.bulk_update(points, ["redemption"])
        except ValueError as error:
            actual_points = get_points_for_user(customer, business)
            expected_points = defaultdict(int)
            for reward in rewards:
                quantity = reward["quantity"]
                rule = reward["rule"]
                currency_id = rule.campaign.currency_id
                expected_points[currency_id] += rule.value * quantity
            return Response(
                {
                    "actual": actual_points,
                    "expected": expected_points,
                    "error": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class HistoryView(APIView):
    @swagger_auto_schema(manual_parameters=[_customer_param, _currency_param])
    def get(self, request):
        currency_id = request.query_params.get("currency")
        customer_id = self.request.query_params.get("customer")
        currency = get_object_or_404(
            Currency.objects.select_related("business"), id=currency_id
        )
        business = currency.business
        customer = get_object_or_404(business.customers, id=customer_id)

        points = (
            Point.objects.filter(user=customer, currency=currency)
            .values("created_at", "expires_at")
            .order_by("-created_at", "-expires_at")
            .annotate(value=Count(Star()))
        )
        redemptions = (
            Redemption.objects.filter(user=customer, currency=currency)
            .values("created_at", "reward", "value")
            .order_by("-created_at")
        )

        # TODO: Preferably do this merging form the db instead of in Python.
        result = heapq.merge(
            points.iterator(),
            redemptions.iterator(),
            key=lambda row: row["created_at"],
            reverse=True,
        )
        return Response(result)
