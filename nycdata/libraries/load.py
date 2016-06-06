import os

from django.contrib.gis.utils import LayerMapping

from livinglots_lots.exceptions import ParcelAlreadyInLot
from livinglots_lots.models import Use
from lots.models import Lot
from ..load import get_processed_data_file
from ..parcels.models import Parcel
from .models import Library, library_mapping


def load(**kwargs):
    from_shapefile(**kwargs)


def from_shapefile(strict=True, progress=True, verbose=False, **kwargs):
    """
    Load library data into the database from the processed shapefile.
    """
    shp = get_processed_data_file(os.path.join('libraries', 'libraries.shp'))
    mapping = LayerMapping(Library, shp, library_mapping, transform=False)
    mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)

    use = Use.objects.get_or_create(
        name='library',
        visible=True,
    )[0]

    # Add parcel to library
    for library in Library.objects.all():
        parcel = None
        if library.bbl:
            try:
                parcel = Parcel.objects.with_bbl(bbl=library.bbl)[0]
            except Exception:
                pass
        if not parcel:
            try:
                parcel = Parcel.objects.get(geom__contains=library.geom)
            except Exception:
                pass
        if parcel:
            library.parcel = parcel
            library.save()

            try:
                lot_kwargs = {
                    'added_reason': 'Loaded with library data',
                    'city': library.city,
                    'commons_content_object': library,
                    'commons_type': 'library',
                    'country': 'USA',
                    'name': library.name,
                    'known_use': use,
                    'known_use_certainty': 8,
                    'known_use_locked': True,
                    'state_province': 'NY',
                }
                lot = Lot.objects.create_lot_for_parcel(parcel, **lot_kwargs)
            except ParcelAlreadyInLot:
                print '\tParcel %s already in a lot. Skipping.' % parcel
                continue
