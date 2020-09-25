from rest_framework import serializers

from dijkstra.models import Map, LogisticNetwork, Endpoint


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ['name']


class LogisticNetworkSerializer(serializers.ModelSerializer):
    origin = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Endpoint.objects.all()
    )
    destiny = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Endpoint.objects.all()
    )

    class Meta:
        model = LogisticNetwork
        fields = ['origin', 'destiny', 'distance']


class MapSerializer(serializers.ModelSerializer):
    networks = LogisticNetworkSerializer(many=True, read_only=False)

    class Meta:
        model = Map
        fields = ['id', 'title', 'networks']
        depth = 2
