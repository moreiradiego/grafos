from rest_framework import viewsets

from dijkstra.api.serializers import MapSerializer, LogisticNetworkSerializer
from dijkstra.models import Map, LogisticNetwork


class LogisticNetworkViewSet(viewsets.ModelViewSet):
    serializer_class = LogisticNetworkSerializer
    queryset = LogisticNetwork.objects.all()


class MapViewSet(viewsets.ModelViewSet):
    serializer_class = MapSerializer
    queryset = Map.objects.prefetch_related('logisticnetwork_set',
                                            'logisticnetwork_set__destiny',
                                            'logisticnetwork_set__origin')
