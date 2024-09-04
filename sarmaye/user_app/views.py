from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegisterSerializer
from django.contrib.auth.models import User

class Login(TokenObtainPairView):
    pass

class Refresh(TokenRefreshView):
    pass

class UserRegisteration(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class UserProfileView(ListAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.get(user = self.request.user)