import django_filters
from app_smart.models import Sensor, TemperaturaData
from rest_framework import permissions
from app_smart.api import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q

class SensorFilter(django_filters.FilterSet):
    responsavel = django_filters.CharFilter(
        field_name='responsavel',
        lookup_expr='icontains'
    )
    
    status_operacional = django_filters.BooleanFilter(
        field_name='status_operacional',
        lookup_expr='exact'
    )
    
    tipo = django_filters.CharFilter(
        field_name='tipo',
        lookup_expr='exact'
    )
    
    localizacao = django_filters.CharFilter(
        field_name='localizacao',
        lookup_expr='icontains'
    )

    class Meta:
        model = Sensor
        fields = ['status_operacional', 'tipo', 'localizacao', 'responsavel']
        
class SensorFilterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tipo = request.data.get('tipo', None)
        localizacao = request.data.get('localizacao', None)
        responsavel = request.data.get('responsavel', None)
        status_operacional = request.data.get('status_operacional', None)

        filters = Q()  # Inicializa um filtro vazio

        if tipo:
            filters &= Q(tipo__icontains=tipo)
        if localizacao:
            filters &= Q(localizacao__icontains=localizacao)
        if responsavel:
            filters &= Q(responsavel__icontains=responsavel)
        if status_operacional is not None:
            filters &= Q(status_operacional=status_operacional)

        # Use a queryset filtrada
        queryset = Sensor.objects.filter(filters)

        # Serialize os dados filtrados
        serializer = serializers.SensorSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)  # Retorna status 200 por padrão

class TemperaturaDataFilter(django_filters.FilterSet):
    timestamp_gte = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_lte = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    sensor = django_filters.NumberFilter(field_name='sensor')
    valor_gte = django_filters.NumberFilter(field_name='valor', lookup_expr='gte')
    valor_lte = django_filters.NumberFilter(field_name='valor', lookup_expr='lte')

    class Meta:
        model = TemperaturaData
        fields = [
            'timestamp_gte',
            'timestamp_lte',
            'sensor',
            'valor_gte',
            'valor_lte'
        ]
