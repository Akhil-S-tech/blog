from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    ActivateSerializer,
)
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
        if self.action == "register":
            self.permission_classes = [AllowAny]
        if self.action == "login":
            self.permission_classes = [AllowAny]
        if self.action == "activate":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        if self.action == "register":
            return UserRegisterSerializer
        if self.action == "login":
            return UserLoginSerializer
        if self.action == "activate":
            return ActivateSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = Profile.objects.filter(Q(user__is_verified=True))
        return queryset

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        password = serializer.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if user.is_verified == False:
            return Response(
                {"error": "Please verify your email"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["POST"])
    def activate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Email verification success"}, status=status.HTTP_200_OK
        )
