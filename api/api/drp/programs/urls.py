from django.urls import path

from rest_framework import routers

from drp.programs import views


router = routers.SimpleRouter()
router.register("businesses", views.BusinessViewSet)
router.register("campaigns", views.CampaignViewSet)
router.register("currencies", views.CurrencyViewSet)

urlpatterns = [
    path(
        "customers/<int:business_id>/",
        views.CustomerListView.as_view(),
        name="customers",
    ),
    path(
        "join/<int:business_id>/", views.JoinProgramView.as_view(), name="join-program"
    ),
    path(
        "leave/<int:business_id>/",
        views.LeaveProgramView.as_view(),
        name="leave-program",
    ),
] + router.urls
