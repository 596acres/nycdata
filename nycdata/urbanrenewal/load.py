import requests

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


def add_urban_renewal_record(record):
    properties = record['properties']
    try:
        urban_renewal_record = UrbanRenewalRecord(
            parcel=Parcel.objects.get(bbl=properties['BBL']),
            disposition_short=properties['disposition_filterable'],
            disposition_long=properties['disposition_display'],
            parking=properties['in_parking'] == 1,
            plan_name=properties['plan_name'],
        )
        urban_renewal_record.save()
        return urban_renewal_record
    except Parcel.DoesNotExist:
        print 'Could not find %s' % properties['BBL']
        return None
    except IntegrityError as e:
        print 'Error adding %s: %s' % (properties['BBL'], e)
        return None
