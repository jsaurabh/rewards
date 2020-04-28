from django.urls import path
from .views import DeleteEmployeeView, AddEmployeeView, EmployeeView

urlpatterns = [
    path("", EmployeeView.as_view(), name = "employeesDashboard"),
    path("delete", DeleteEmployeeView.as_view(), name = "deleteEmployees"),
    path("add", AddEmployeeView.as_view(), name = "addEmployees"),
]
