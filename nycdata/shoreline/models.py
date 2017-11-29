# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class Shoreline(models.Model):
    fid = models.BigIntegerField()
    geom = models.MultiLineStringField(srid=4326)


# Auto-generated `LayerMapping` dictionary for Shoreline model
shoreline_mapping = {
    'fid': 'FID',
    'geom': 'MULTILINESTRING',
}
