import json
import requests

from django.contrib.gis.db.models.functions import Area, Intersection, Transform
from django.contrib.gis.geos import GEOSGeometry
from django.db import IntegrityError

from ..parcels.models import Parcel
from .models import UrbanRenewalRecord


urban_reviewer_data_url = 'https://github.com/596acres/urbanreviewer/raw/gh-pages/data/geojson/us/ny/nyc/nyc.geojson'


def load(**kwargs):
    from_github(**kwargs)


def from_github(verbose=False, **kwargs):
    """
    Load urban renewal data from GitHub.

    Download the latest NYC data from the Urban Reviewer GitHub repo. For each
    parcel in the data, add an UrbanRenewalRecord with the plan name and
    disposition.
    """
    # Download latest GeoJSON 
    urban_renewal_parcels = requests.get(urban_reviewer_data_url).json()['features']

    for urban_renewal_parcel in urban_renewal_parcels:
        add_urban_renewal_record(urban_renewal_parcel)


def get_parcel(record):
    parcel = None
    bbl = record['properties']['BBL']

    try:
        parcel = Parcel.objects.get(bbl=bbl)
    except Parcel.DoesNotExist:
        polygon = GEOSGeometry(json.dumps(record['geometry']))
        try:
            parcel = Parcel.objects.filter(geom__overlaps=polygon).annotate(
                intersect_area=Area(Transform(Intersection('geom', polygon), 2263))
            ).order_by('-intersect_area')[0]
        except IndexError:
            # No parcel found, None will be returned
            pass
    return parcel


def add_urban_renewal_record(record):
    properties = record['properties']
    parcel = get_parcel(record)

    if not parcel:
        print 'No parcel for %s, skipping' % properties['BBL']
        return None

    try:
        urban_renewal_record = UrbanRenewalRecord(
            parcel=parcel,
            disposition_short=properties['disposition_filterable'],
            disposition_long=properties['disposition_display'],
            parking=properties['in_parking'] == 1,
            plan_name=properties['plan_name'],
        )
        urban_renewal_record.save()
        return urban_renewal_record
    except IntegrityError as e:
        # Parcel already associated with an Urban Renewal Record
        return None
