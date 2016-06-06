# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class Library(models.Model):
    bbl = models.CharField(max_length=254)
    housenum = models.CharField(max_length=254)
    borocode = models.FloatField()
    bin = models.FloatField()
    zip = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    system = models.CharField(max_length=254)
    url = models.URLField()
    streetname = models.CharField(max_length=254)
    geom = models.PointField(srid=4326)
    objects = models.GeoManager()


# Auto-generated `LayerMapping` dictionary for Library model
library_mapping = {
    'bbl' : 'bbl',
    'housenum' : 'housenum',
    'borocode' : 'borocode',
    'bin' : 'bin',
    'zip' : 'zip',
    'city' : 'city',
    'name' : 'name',
    'system' : 'system',
    'url' : 'url',
    'streetname' : 'streetname',
    'geom' : 'POINT',
}
