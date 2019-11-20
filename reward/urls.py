from django.urls import path
from .views import RewardsView, AccRulesView, RedRulesView, DeleteCampaign, AddCampaign, EditCampaign, CurrencyView
from .views import DeleteAccRules, AddAccRules, EditAccRules
from .views import DeleteRedRules, AddRedRules, EditRedRules
from .views import DeleteCurrency, AddCurrency, EditCurrency

urlpatterns = [
    path("", RewardsView.as_view(), name = "rewardDashboard"),
    path("accRules", AccRulesView.as_view(), name = "itemsDashboard"),
    path("redRules", RedRulesView.as_view(), name = "itemsDashboard"),
    path("currency", CurrencyView.as_view(), name = "currencyDashboard"),
    path("delete", DeleteCampaign.as_view(), name = "deleteCategories"),
    path("add", AddCampaign.as_view(), name = "addCategories"),
    path("edit", EditCampaign.as_view(), name = "editCategories"),
    path("deleteAccRules", DeleteAccRules.as_view(), name = "deleteItems"),
    path("addAccRules", AddAccRules.as_view(), name = "deleteItems"),
    path("editAccRules", EditAccRules.as_view(), name = "deleteItems"),
    path("deleteRedRules", DeleteRedRules.as_view(), name = "deleteItems"),
    path("addRedRules", AddRedRules.as_view(), name = "deleteItems"),
    path("editRedRules", EditRedRules.as_view(), name = "deleteItems"),
    path("deleteCurrency", DeleteCurrency.as_view(), name = "deleteItems"),
    path("addCurrency", AddCurrency.as_view(), name = "deleteItems"),
    path("editCurrency", EditCurrency.as_view(), name = "deleteItems"),
]
