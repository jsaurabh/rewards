from django.urls import path
from .views import DeleteCategoryView, AddCategoryView, EditCategoryView, CatalogView
from .views import AddItemsView, EditItemsView, DeleteItemsView
from .views import ItemView

urlpatterns = [
    path("", CatalogView.as_view(), name = "catalogDashboard"),
    path("items", ItemView.as_view(), name = "itemsDashboard"),
    path("delete", DeleteCategoryView.as_view(), name = "deleteCategories"),
    path("add", AddCategoryView.as_view(), name = "addCategories"),
    path("edit", EditCategoryView.as_view(), name = "editCategories"),
    path("delete-items", DeleteItemsView.as_view(), name = "deleteItems"),
    path("add-items", AddItemsView.as_view(), name = "addItems"),
    path("edit-items", EditItemsView.as_view(), name = "edittems"),
]
