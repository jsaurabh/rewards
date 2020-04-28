from django.urls import path

from rest_framework import routers

from drp.users import views


router = routers.SimpleRouter()
router.register("", views.UserViewSet)

urlpatterns = [
    path("auth/change-password/", views.ChangePasswordView.as_view()),
    path("auth/login/", views.LoginView.as_view()),
] + router.urls
