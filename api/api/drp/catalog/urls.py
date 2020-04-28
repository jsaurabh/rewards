from django.urls import path
from rest_framework import routers

from drp.catalog import views


router = routers.SimpleRouter()
router.register("categories", views.CategoryViewSet)
router.register("items", views.ItemViewSet)

urlpatterns = [
    path(
        "business/<int:business_id>/",
        views.BusinessCatalogView.as_view(),
        name="business-catalog",
    )
] + router.urls
