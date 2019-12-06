from django.urls import path
from django.views.generic.base import TemplateView
from .views import DashView, BusinessCreate, BusinessEditView, BusinessView, BusinessDeleteView
from django.contrib.auth.decorators import login_required

from .forms import BusinessCreateWizard, AddCurrencyWizard
from .views import FormWizardView

urlpatterns = [
    path("wizard", FormWizardView.as_view([BusinessCreateWizard, AddCurrencyWizard]), name = "dashboard1"),
    path("", login_required(DashView.as_view()), name = "dash"),
    path("business", BusinessView.as_view(), name = "business"),   
    path("add", BusinessCreate.as_view(), name = 'add_business'),
    path("delete", BusinessDeleteView.as_view(), name = "deleteBusiness"),
    path("edit", BusinessEditView.as_view(), name = 'edit_business'),
]