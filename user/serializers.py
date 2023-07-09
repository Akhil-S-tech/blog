from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

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
