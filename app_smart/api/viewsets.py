from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from app_smart.api import serializers
from app_smart.models import Sensor  # Importando diretamente do models.py
from app_smart.api.filters import SensorFilter

class CreateUserAPIViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = [permissions.IsAdminUser]  # Descomente se necessário

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SensorFilter
