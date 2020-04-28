from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drp.users.models import User
from drp.users.permissions import IsAdminOrSelf
from drp.users.serializers import (
    ChangePasswordSerializer,
    UserSerializer,
    UserRegistrationSerializer,
)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data,})


class UserViewSet(ModelViewSet):
    permission_classes = [IsAdminOrSelf]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request, format=None):
        serializer = UserRegistrationSerializer(
            data=request.data, context={"user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        data = {**serializer.validated_data}
        if "phone" in data and not data["phone"]:
            del data["phone"]
        user = User.objects.create_user(**data)
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data,})


class ChangePasswordView(APIView):
    def get_serializer(self):
        return ChangePasswordSerializer(
            data=self.request.data, context={"user": self.request.user},
        )

    @swagger_auto_schema(responses={status.HTTP_204_NO_CONTENT: "Success"})
    def post(self, request):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
