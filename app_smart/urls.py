from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app_smart.api.viewsets import CreateUserAPIViewSet, SensorViewSet
from . import views

router = DefaultRouter()
router.register(r'sensores', SensorViewSet)

urlpatterns = [
    path('', views.abre_index, name='abre_index'),
    path('api/create_user/', CreateUserAPIViewSet.as_view(), name='create_user'),
    path('api/', include(router.urls)),
]
