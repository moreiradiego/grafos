from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from dijkstra.api.serializers import MapSerializer, LogisticNetworkSerializer, EndpointSerializer
from dijkstra.models import Map, LogisticNetwork, Endpoint


class EndpointViewSet(viewsets.ModelViewSet):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class LogisticNetworkViewSet(viewsets.ModelViewSet):
    serializer_class = LogisticNetworkSerializer
    queryset = LogisticNetwork.objects.all()


def make_graph(map):
    base_map = Map.objects.get(pk=map)
    base_edges = Endpoint.objects.filter(Q(origin__in=base_map.networks.all()) | Q(destiny__in=base_map.networks.all())).distinct()
    base_graph = {}

    for edge in base_edges:
        base_graph.update({edge.name: {}})

    for vertice in base_map.networks.all():
        base_graph[vertice.origin.name][vertice.destiny.name] = vertice.distance

    return base_graph


class MapViewSet(viewsets.ModelViewSet):
    serializer_class = MapSerializer
    queryset = Map.objects.all()

    def create(self, request, *args, **kwargs):
        data = self.request.data

        new_map = Map.objects.create()
        new_map.title = data['title']
        for endpoint_data in data['networks']:
            origin_endpoint = Endpoint.objects.create(name=endpoint_data['origin'])
            destiny_endpoint = Endpoint.objects.create(name=endpoint_data['destiny'])
            distance = endpoint_data['distance']
            new_edge = LogisticNetwork.objects.create(
                origin=origin_endpoint,
                destiny=destiny_endpoint,
                distance=distance
            )
            new_map.networks.add(new_edge)
        new_map.save()
        serializer = MapSerializer(new_map)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def calcular(self, request, pk=None):
        base_graph = make_graph(pk)
        start = self.request.data['inicio']
        goal = self.request.data['fim']
        fuel_range = int(self.request.data['autonomia'])
        fuel_price = float(self.request.data['valor_litro'])
        shortest_distance = {}
        predecessor = {}
        unseen_nodes = base_graph
        infinity = 9999999999999
        path = []
        for node in unseen_nodes:
            shortest_distance[node] = infinity
        shortest_distance[start] = 0

        while unseen_nodes:
            min_node = None
            for node in unseen_nodes:
                if min_node is None:
                    min_node = node
                elif shortest_distance[node] < shortest_distance[min_node]:
                    min_node = node

            for child_node, weight in base_graph[min_node].items():
                if weight + shortest_distance[min_node] < shortest_distance[child_node]:
                    shortest_distance[child_node] = weight + shortest_distance[min_node]
                    predecessor[child_node] = min_node
            unseen_nodes.pop(min_node)

        current_node = goal
        while current_node != start:
            try:
                path.insert(0, current_node)
                current_node = predecessor[current_node]
            except KeyError:
                return Response({"Error": "Path no reachable"}, status=status.HTTP_412_PRECONDITION_FAILED)
        if shortest_distance[goal] != infinity:
            path.insert(0, start)
            shortest_distance = shortest_distance[goal]
            fuel_cost = (shortest_distance / float(fuel_range)) * float(fuel_price)
            str_path = ''.join(path).upper()
        return Response({"rota": str_path, "custo": fuel_cost})
