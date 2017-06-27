import os

from django.contrib.gis.utils import LayerMapping

from livinglots_lots.exceptions import ParcelAlreadyInLot
from lots.models import Lot
from owners.models import Owner
from ..load import get_processed_data_file
from ..parcels.models import Parcel
from .models import Landmark, landmark_mapping


def load(**kwargs):
    from_shapefile(**kwargs)


def add_landmarks_to_parcels():
    # Add landmark to parcel
    for landmark in Landmark.objects.filter(status='DESIGNATED', parcel__isnull=True):
        parcel = None
        if landmark.bbl:
            try:
                parcel = Parcel.objects.with_bbl(bbl=landmark.bbl)[0]
            except Exception:
                pass
        if not parcel:
            try:
                parcel = Parcel.objects.get(geom__contains=landmark.geom)
            except Exception:
                pass
        if parcel:
            landmark.parcel = parcel
            landmark.save()


def from_shapefile(strict=True, progress=True, verbose=False, **kwargs):
    """
    Load landmark data into the database from the processed shapefile.
    """
    shp = get_processed_data_file(os.path.join('landmarks', 'landmarks.shp'))
    mapping = LayerMapping(Landmark, shp, landmark_mapping, transform=False)
    mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)

    add_landmarks_to_parcels()
