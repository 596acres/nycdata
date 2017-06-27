# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

# This is an auto-generated Django model module created by ogrinspect.
class Landmark(models.Model):
    name = models.CharField(max_length=254)
    non_bldg = models.CharField(max_length=254)
    last_action = models.CharField(max_length=254)
    historic_district = models.CharField(max_length=254)
    secnd_bldg = models.FloatField()
    objectid = models.FloatField()
    calen_date = models.CharField(max_length=254)
    block = models.FloatField()
    date_designated = models.DateField()
    time_designated = models.CharField(max_length=254)
    most_current = models.FloatField()
    vacant_lot = models.FloatField()
    boundaries = models.CharField(max_length=254)
    bin_number = models.FloatField()
    pluto_addr = models.CharField(max_length=254)
    status_not = models.CharField(max_length=254)
    status = models.CharField(max_length=254)
    lot = models.FloatField()
    lm_type = models.CharField(max_length=254)
    other_hear = models.CharField(max_length=254)
    desig_addr = models.CharField(max_length=254)
    lp_number = models.CharField(max_length=254)
    public_hea = models.CharField(max_length=254)
    borough_id = models.CharField(max_length=254)
    count_bldg = models.FloatField()
    bbl = models.CharField(max_length=254)
    geom = models.PointField(srid=4326)
    parcel = models.ForeignKey('parcels.Parcel',
        related_name='landmark_object',
        blank=True,
        null=True
    )
    objects = models.GeoManager()

    def _get_report_url(self):
        number = self.lp_number.split('-')[1][-4:]
        return 'http://s-media.nyc.gov/agencies/lpc/lp/%s.pdf' % number
    report_url = property(_get_report_url)


# Auto-generated `LayerMapping` dictionary for Landmark model
landmark_mapping = {
    'name' : 'lm_name',
    'non_bldg' : 'non_bldg',
    'last_action' : 'last_actio',
    'historic_district' : 'hist_distr',
    'secnd_bldg' : 'secnd_bldg',
    'objectid' : 'objectid',
    'calen_date' : 'calen_date',
    'block' : 'block',
    'date_designated' : 'date_desig',
    'time_designated' : 'time_desig',
    'most_current' : 'most_curre',
    'vacant_lot' : 'vacant_lot',
    'boundaries' : 'boundaries',
    'bin_number' : 'bin_number',
    'pluto_addr' : 'pluto_addr',
    'status_not' : 'status_not',
    'status' : 'status',
    'lot' : 'lot',
    'lm_type' : 'lm_type',
    'other_hear' : 'other_hear',
    'desig_addr' : 'desig_addr',
    'lp_number' : 'lp_number',
    'public_hea' : 'public_hea',
    'borough_id' : 'borough_id',
    'count_bldg' : 'count_bldg',
    'bbl' : 'bbl',
    'geom' : 'POINT',
}
