from django.contrib.gis.db import models


class WaterfrontParcel(models.Model):
    bbl = models.FloatField()
    ownerfixed = models.CharField(max_length=254, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()


waterfront_parcel_mapping = {
    'bbl' : 'BBL',
    'ownerfixed' : 'OwnerFixed',
    'geom' : 'MULTIPOLYGON',
}
