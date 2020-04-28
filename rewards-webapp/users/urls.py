from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView

from .views import UserView

urlpatterns = [
    path("", login_required(UserView.as_view()), name = "user"),
]