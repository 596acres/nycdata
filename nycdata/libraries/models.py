# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class Library(models.Model):
    bbl = models.CharField(max_length=254)
    housenum = models.CharField(max_length=254)
    bin = models.FloatField()
    zip = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    system = models.CharField(max_length=254)
    url = models.URLField()
    streetname = models.CharField(max_length=254)
    public = models.CharField(max_length=254, blank=True, null=True)
    ownerfixed = models.CharField(max_length=254, blank=True, null=True)
    geom = models.PolygonField(srid=4326)
    objects = models.GeoManager()


# Auto-generated `LayerMapping` dictionary for Library model
library_mapping = {
    'bbl' : 'bbl_string',
    'housenum' : 'housenum',
    'bin' : 'bin',
    'zip' : 'zip',
    'city' : 'city',
    'name' : 'name',
    'system' : 'system',
    'url' : 'url',
    'streetname' : 'streetname',
    'public' : 'public',
    'ownerfixed' : 'OwnerFixed',
    'geom' : 'POLYGON',
}
