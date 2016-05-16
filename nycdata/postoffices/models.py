from django.contrib.gis.db import models


# This is an auto-generated Django model module created by ogrinspect.
class PostOffice(models.Model):
    parcel = models.ForeignKey('parcels.Parcel', blank=True, null=True)
    name = models.CharField(max_length=254)
    streetname = models.CharField(max_length=254)
    url = models.CharField(max_length=254)
    housenum = models.CharField(max_length=254)
    bin = models.FloatField()
    zip = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    bbl = models.CharField(max_length=254)
    geom = models.PointField(srid=4326)
    objects = models.GeoManager()


# Auto-generated `LayerMapping` dictionary for PostOffice model
postoffice_mapping = {
    'name' : 'name',
    'streetname' : 'streetname',
    'url' : 'url',
    'housenum' : 'housenum',
    'bin' : 'bin',
    'zip' : 'zip',
    'city' : 'city',
    'bbl' : 'bbl',
    'geom' : 'POINT',
}
