from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from app_smart.api import serializers
from app_smart.models import Sensor, TemperaturaData
from app_smart.api.filters import SensorFilter, TemperaturaDataFilter, SensorFilterView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd


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

class UploadExcelView(APIView):
    queryset = Sensor.objects.all()
    serializer_class = serializers.UploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Verificando se o arquivo está presente
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.xlsx'):
            return Response({'error': 'Arquivo não é um Excel válido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Lendo o arquivo Excel
            df = pd.read_excel(file)

            for _, row in df.iterrows():
                # Preparando os dados do sensor
                sensor_data = {
                    'tipo': row['tipo'],
                    'unidade_medida': row['unidade_medida'] if row['unidade_medida'] else None,
                    'latitude': float(row['latitude']) if isinstance(row['latitude'], (float, int)) else float(row['latitude'].replace(',', '.')),
                    'longitude': float(row['longitude']) if isinstance(row['longitude'], (float, int)) else float(row['longitude'].replace(',', '.')),
                    'localizacao': row['localizacao'],
                    'responsavel': row['responsavel'] if row['responsavel'] else '',
                    'status_operacional': True if row['status_operacional'] == 'True' else False,
                    'observacao': row['observacao'] if row['observacao'] else '',
                    'mac_address': row['mac_address'] if row['mac_address'] else None,
                }


                # Validando e salvando os dados
                serializer = serializers.SensorSerializer(data=sensor_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Sensores registrados com sucesso!'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TemperaturaDataViewSet(viewsets.ModelViewSet):
    queryset = TemperaturaData.objects.all()
    serializer_class = serializers.TemperaturaDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TemperaturaDataFilter