from django.urls import path

from .views import DashView

urlpatterns = [
    path("", DashView.as_view(), name = "dash")
]