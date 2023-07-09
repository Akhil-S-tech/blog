from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Profile
from .email import send_email_verification, email_verification_success
from .utils import decode_uid
from .tokens import email_verification_token

USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "name",
            "username",
            "email",
            "avatar",
            "bio",
            "created_at",
            "updated_at",
        )
        excludes = ("user",)


class UserRegisterSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirm_password"] = serializers.CharField(
            style={"input_type": "password"}, write_only=True
        )

    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = USER
        fields = ("id", "username", "name", "email", "password")

    def validate(self, attrs):
        self.fields.pop("confirm_password", None)
        confirm_password = attrs.pop("confirm_password", None)
        password = attrs.get("password")

        user = USER(**attrs)
        if password == confirm_password:
            try:
                validate_password(password, user)
            except ValidationError as e:
                error = serializers.as_serializer_error(e)
                raise serializers.ValidationError(error)
            return attrs
        else:
            raise serializers.ValidationError("Password not matching.")

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            raise ValueError("Cannot create user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = USER.objects.create_user(**validated_data)
            send_email_verification(user)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(style={"input_type": "password"})
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        return super().validate(attrs)


class UidSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = decode_uid(attrs.get("uid"))
            self.user = USER.objects.get(id=uid)
        except:
            self.user = None

        if self.user is not None:
            if self.user and email_verification_token.check_token(
                self.user, attrs.get("token")
            ):
                self.user.is_verified = True
                self.user.save()
                email_verification_success(self.user)
                return super().validate(attrs)
        else:
            raise serializers.ValidationError("Invalid link or link expired")


class ActivateSerializer(UidSerializer):
    pass


class CurrentPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    def validate_current_password(self, value):
        is_valid_password = self.context["request"].user.check_password(value)

        if is_valid_password:
            return value
        return ValidationError("Invalid password")
