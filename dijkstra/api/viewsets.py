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
    base_edges = Endpoint.objects.filter(
        Q(origin__in=base_map.networks.all()) | Q(destiny__in=base_map.networks.all())).distinct()
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

    @action(methods=['POST'], detail=False)
    def importar(self, request, *args, **kwargs):
        uploaded_file = self.request.FILES['mapa']
        lines = uploaded_file.readlines()
        map_object = Map.objects.create()
        for ln in lines:
            list_index = lines.index(ln)
            if list_index == 0:
                map_object.title = ln
            else:
                line_obj = ln.split()
                if len(line_obj) > 3:
                    return Response(
                        {"Error": "Linha Inválida. O mapa deve ser expresso no padrão \"ORIGEM DESTINO DISTANCIA\""},
                        status=status.HTTP_412_PRECONDITION_FAILED)
                if line_obj[0].decode('utf-8').lower() == line_obj[1].decode('utf-8').lower():
                    return Response(
                        {"Error": "Linha Inválida. A origem deve ser diferente do destino."},
                        status=status.HTTP_412_PRECONDITION_FAILED)
                point_origin, created = Endpoint.objects.get_or_create(
                    name=line_obj[0].decode('utf-8').lower()
                )
                point_destiny, created = Endpoint.objects.get_or_create(
                    name=line_obj[1].decode('utf-8').lower()
                )
                distance = line_obj[2].decode('utf-8').lower()
                new_edge, created = LogisticNetwork.objects.get_or_create(
                    origin=point_origin.id,
                    destiny=point_destiny.id,
                    distance=distance
                )
                map_object.networks.add(new_edge)
        map_object.save()
        serializer = MapSerializer(map_object)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def calcular(self, request, pk=None):

        base_graph = make_graph(pk)
        start = self.request.POST.get('inicio', next(iter(base_graph)))
        goal = self.request.POST.get('fim', next(reversed(base_graph)))
        fuel_range = self.request.POST.get('autonomia', 0)
        fuel_price = self.request.POST.get('valor_litro', 0)
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
            if fuel_range == 0 or fuel_price == 0:
                fuel_cost = "Gasro de combustível não solicitado. Por favor, preencha a autonomia e o valor por litro"
            else:
                fuel_cost = (shortest_distance / float(fuel_range)) * float(fuel_price)
            str_path = ''.join(path).upper()
        return Response({"rota": str_path, "custo": fuel_cost})
