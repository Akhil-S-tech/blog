from rest_framework import generics, viewsets, status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import Profile
from django.db.models import Q

USER = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = Profile.objects.filter(Q(user__is_verified=True))
        return queryset

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
