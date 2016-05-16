import os

from django.contrib.gis.utils import LayerMapping

from ..load import get_processed_data_file
from ..parcels.models import Parcel
from .models import PostOffice, postoffice_mapping


def load(**kwargs):
    from_shapefile(**kwargs)


def from_shapefile(strict=True, progress=True, verbose=False, **kwargs):
    """
    Load post office data into the database from the processed shapefile.
    """
    shp = get_processed_data_file(os.path.join('postoffices', 'postoffices.shp'))
    mapping = LayerMapping(PostOffice, shp, postoffice_mapping,
                           transform=False)
    mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)

    # Add parcel to post office
    for post_office in PostOffice.objects.all():
        parcel = None
        if post_office.bbl:
            try:
                parcel = Parcel.objects.with_bbl(bbl=post_office.bbl)[0]
            except Exception:
                pass
        if not parcel:
            try:
                parcel = Parcel.objects.get(geom__contains=post_office.geom)
            except Exception:
                pass
        if parcel:
            post_office.parcel = parcel
            post_office.save()
