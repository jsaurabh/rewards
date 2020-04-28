from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from drp.programs.serializers import BusinessSerializer
from drp.users.models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class UserSerializer(serializers.ModelSerializer):
    customer_of = BusinessSerializer(many=True, read_only=True)
    employee_of = BusinessSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "customer_of",
            "employee_of",
        )


class UserRegistrationSerializer(UserSerializer):
    password = serializers.CharField(
        trim_whitespace=False, write_only=True, style={"input_type": "password"},
    )

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("password",)

    def validate_password(self, value):
        validate_password(value, self.context["user"])
        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        trim_whitespace=False, write_only=True, style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        trim_whitespace=False, write_only=True, style={"input_type": "password"},
    )

    @property
    def _user(self):
        return self.context["user"]

    def validate_current_password(self, value):
        if not self._user.check_password(value):
            raise serializers.ValidationError(
                "The current password provided is incorrect."
            )
        return value

    def validate_new_password(self, value):
        validate_password(value, self._user)
        return value

    def save(self):
        new_password = self.validated_data["new_password"]
        self._user.set_password(new_password)
        self._user.save()
