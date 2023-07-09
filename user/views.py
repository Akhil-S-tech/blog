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
from .email import send_email_verification
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    ActivateSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    SetNewPasswordSerializer,
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
        if self.action == "reset_password":
            self.permission_classes = [IsAuthenticated]
        if self.action == "forgot_password":
            self.permission_classes = [AllowAny]
        if self.action == "set_password":
            self.permission_classes = [AllowAny]
        if self.action == "me":
            self.permission_classes = [IsAuthenticated]
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
        if self.action == "reset_password":
            return ChangePasswordSerializer
        if self.action == "forgot_password":
            return ForgotPasswordSerializer
        if self.action == "set_password":
            return SetNewPasswordSerializer
        if self.action == "me":
            return UserSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = Profile.objects.filter(Q(user__is_verified=True))
        return queryset

    def get_instance(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET", "DELETE"])
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            serializer = self.get_serializer(self.get_object().profile, many=False)
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
                {"error": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND
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

    @action(detail=False, methods=["POST"])
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_instance()
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(
            {"message": "password changes successfuly"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["POST"])
    def forgot_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = USER.objects.filter(email=serializer.data.get("email")).first()

        if user is None:
            return Response(
                {"message": "Email not fount"}, status=status.HTTP_404_NOT_FOUND
            )
        if user.is_verified == False:
            return Response(
                {"message": "Please verify your email"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        send_email_verification(user)
        return Response(
            {"message": f"Email send seccessfully {user.email}"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["POST"])
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(
            {"message": "Password set successfully"}, status=status.HTTP_200_OK
        )
