from django.urls import path
from rest_framework import routers

from drp.rewards import views


router = routers.SimpleRouter()
router.register("accumulation-rules", views.AccumulationRuleViewSet)
router.register("redemption-rules", views.RedemptionRuleViewSet)

urlpatterns = [
    path("redeem/", views.RedeemView.as_view(), name="redeem"),
    path("history/", views.HistoryView.as_view(), name="history"),
] + router.urls
