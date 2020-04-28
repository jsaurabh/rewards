from django.urls import path

from drp.orders import views


urlpatterns = [
    path("", views.OrderView.as_view(), name="order"),
]
