from rest_framework import serializers

from dijkstra.models import Map, LogisticNetwork


class LogisticNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticNetwork
        fields = '__all__'


class MapSerializer(serializers.ModelSerializer):
    logisticnetwork = LogisticNetworkSerializer(many=True, read_only=True)

    class Meta:
        model = Map
        fields = '__all__'
