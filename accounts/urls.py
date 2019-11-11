from django.urls import path
from .views import LoginView, RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(), name = "login"),
    path("register/", RegisterView.as_view(), name = "register"),
    #path("", login_view, name = "login_none"),
    #path("logout/", logout_view, name = "logout"),
]
