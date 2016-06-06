from django.contrib.gis.db import models


# This is an auto-generated Django model module created by ogrinspect.
class NYCHADevelopment(models.Model):
    name = models.CharField(max_length=100)
    borough = models.CharField(max_length=13)
    tds_num = models.CharField(max_length=3)
    nonresidential_buildings = models.IntegerField()
    residential_buildings = models.IntegerField()
    units_in_2011 = models.IntegerField()
    population_in_2011 = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()


# Auto-generated `LayerMapping` dictionary for NYCHADevelopment model
nychadevelopment_mapping = {
    'name' : 'developmen',
    'borough' : 'borough',
    'tds_num' : 'tds_num',
    'nonresidential_buildings' : 'nonres_bld',
    'residential_buildings' : 'res_bldg',
    'units_in_2011' : 'cur_unit11',
    'population_in_2011' : 'tot_pop11',
    'geom' : 'MULTIPOLYGON',
}
