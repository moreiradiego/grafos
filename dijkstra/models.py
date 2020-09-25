from django.db import models


class Endpoint(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Point"
        verbose_name_plural = "Points"


class LogisticNetwork(models.Model):
    origin = models.ForeignKey(Endpoint, null=False, blank=False, on_delete=models.PROTECT, related_name="origin")
    destiny = models.ForeignKey(Endpoint, null=False, blank=False, on_delete=models.PROTECT, related_name="destiny")
    distance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.origin.name) + " to " + str(self.destiny.name)


class Map(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    networks = models.ManyToManyField('dijkstra.LogisticNetwork', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Map"
        verbose_name_plural = "Maps"
