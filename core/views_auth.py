# core/views_auth.py
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers_auth import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer