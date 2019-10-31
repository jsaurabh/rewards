from django.urls import path
from django.views.generic.base import TemplateView
from .views import DashView #EmptyView

urlpatterns = [
    path("", DashView.as_view(), name = "dash"),
    #path("/blank", EmptyView.as_view(), name = 'empty'),
    #path("/blank", TemplateView.as_view(template_name='blank.html'),
]