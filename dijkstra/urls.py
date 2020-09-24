from django.urls import path, include
from rest_framework import routers

from dijkstra.api.viewsets import MapViewSet, LogisticNetworkViewSet

router = routers.DefaultRouter()
router.register(r'mapas', MapViewSet, basename="MapViewSet")
router.register(r'malha', LogisticNetworkViewSet, basename="LogisticNetworkViewSet")

urlpatterns = [
    path('', include(router.urls)),
]