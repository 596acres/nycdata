# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class Park(models.Model):
    location = models.CharField(max_length=254)
    communityb = models.CharField(max_length=254)
    nys_senate = models.CharField(max_length=254)
    signname = models.CharField(max_length=254)
    zipcode = models.CharField(max_length=254)
    us_congres = models.CharField(max_length=254)
    gispropnum = models.CharField(max_length=254)
    borough = models.CharField(max_length=254)
    waterfront = models.CharField(max_length=254)
    nys_assemb = models.CharField(max_length=254)
    councildis = models.CharField(max_length=254)
    acres = models.FloatField()
    typecatego = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()


# Auto-generated `LayerMapping` dictionary for Park model
park_mapping = {
    'location' : 'location',
    'communityb' : 'communityb',
    'nys_senate' : 'nys_senate',
    'signname' : 'signname',
    'zipcode' : 'zipcode',
    'us_congres' : 'us_congres',
    'gispropnum' : 'gispropnum',
    'borough' : 'borough',
    'waterfront' : 'waterfront',
    'nys_assemb' : 'nys_assemb',
    'councildis' : 'councildis',
    'acres' : 'acres',
    'typecatego' : 'typecatego',
    'address' : 'address',
    'geom' : 'MULTIPOLYGON',
}
