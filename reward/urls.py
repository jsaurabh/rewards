from django.urls import path
from .views import RewardsView, RulesView, DeleteCampaign, AddCampaign, EditCampaign
from .views import DeleteAccRules, AddAccRules, EditAccRules
from .views import DeleteRedRules, AddRedRules, EditRedRules
from .views import DeleteCurrency, AddCurrency, EditCurrency

urlpatterns = [
    path("", RewardsView.as_view(), name = "rewardDashboard"),
    path("rules", RulesView.as_view(), name = "itemsDashboard"),
    path("delete", DeleteCampaign.as_view(), name = "deleteCategories"),
    path("add", AddCampaign.as_view(), name = "addCategories"),
    path("edit", EditCampaign.as_view(), name = "editCategories"),
    path("delete-acc-rules", DeleteAccRules.as_view(), name = "deleteItems"),
    path("add-acc-rules", AddAccRules.as_view(), name = "deleteItems"),
    path("edit-acc-rules", EditAccRules.as_view(), name = "deleteItems"),
    path("delete-red-rules", DeleteRedRules.as_view(), name = "deleteItems"),
    path("add-red-rules", AddRedRules.as_view(), name = "deleteItems"),
    path("edit-red-rules", EditRedRules.as_view(), name = "deleteItems"),
    path("delete-currency", DeleteCurrency.as_view(), name = "deleteItems"),
    path("add-currency", AddCurrency.as_view(), name = "deleteItems"),
    path("edit-currency", EditCurrency.as_view(), name = "deleteItems"),
]
