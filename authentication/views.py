from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from .models import CustomUser

from authentication.serializers import MyTokenObtainPairSerializer

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer





class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # Allow any user to register
