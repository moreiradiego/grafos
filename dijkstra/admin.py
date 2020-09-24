from django.contrib import admin

from dijkstra.models import Endpoint
from dijkstra.models import LogisticNetwork
from dijkstra.models import Map

admin.site.register(Map)
admin.site.register(Endpoint)
admin.site.register(LogisticNetwork)
