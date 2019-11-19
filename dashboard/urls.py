from django.urls import path
from django.views.generic.base import TemplateView
from .views import DashView, BusinessCreate, BusinessEditView, BusinessView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", DashView.as_view(), name = "dashboard"),
    #path("", login_required(DashView.as_view()), name = "dash"),
    path("business", BusinessView.as_view(), name = "business"),   
    path("add", BusinessCreate.as_view(), name = 'add_business'),
    path("edit", BusinessEditView.as_view(), name = 'edit_business'),
]