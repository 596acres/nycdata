import os

from django.contrib.gis.utils import LayerMapping

from ..load import get_processed_data_file
from .models import Parcel, parcel_mapping


def from_shapefile(strict=True, progress=True, verbose=False, **kwargs):
    """
    Load parcel data into the database from the processed shapefile.
    """
    boroughs = ('Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten_Island')
    for borough in boroughs:
        parcel_shp = get_processed_data_file(os.path.join('parcels', '%s.shp' % borough))
        mapping = LayerMapping(Parcel, parcel_shp, parcel_mapping, transform=False)
        mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)


def load(**kwargs):
    from_shapefile(**kwargs)

    print 'Adding centroids...'
    total = Parcel.objects.filter(centroid__isnull=True).count()
    updated = 0

    while updated < total:
        to_update = Parcel.objects.filter(centroid__isnull=True).centroid()[:1000]
        for parcel in to_update:
            parcel.centroid = parcel.centroid
            parcel.save()
        updated += to_update.count()
        print '...%d' % updated
