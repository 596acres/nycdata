import os

from django.contrib.gis.utils import LayerMapping

from livinglots_lots.models import Use
from lots.models import Lot
from ..load import get_processed_data_file
from .models import NYCHADevelopment, nychadevelopment_mapping


def load(**kwargs):
    from_shapefile(**kwargs)


def from_shapefile(create_lots=True, strict=True, progress=True, verbose=False, **kwargs):
    """
    Load NYCHA data into the database from the processed shapefile.
    """
    shp = get_processed_data_file(os.path.join('nycha', 'nycha.shp'))
    mapping = LayerMapping(NYCHADevelopment, shp, nychadevelopment_mapping,
                           transform=False)
    mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)

    if create_lots:
        create_lots_for_nycha()


def create_lots_for_nycha():
    use = Use.objects.get_or_create(
        name='NYCHA',
        visible=True,
    )[0]

    for nycha_development in NYCHADevelopment.objects.all():
        print 'Adding lot for NYCHA development %s' % nycha_development.name

        lot_kwargs = {
            'added_reason': 'Loaded with NYCHA data',
            'borough': nycha_development.borough.title(),
            'city': nycha_development.borough.title(),
            'commons_content_object': nycha_development,
            'commons_type': 'NYCHA',
            'country': 'USA',
            'name': nycha_development.name,
            'known_use': use,
            'known_use_certainty': 8,
            'known_use_locked': True,
            'state_province': 'NY',
        }

        # NB: NYCHA developments often span multiple parcels or portions of
        # parcels, so we add them as drawn geometries here rather than tie them
        # to particular parcels.
        lot = Lot.objects.create_lot_for_geom(nycha_development.geom, **lot_kwargs)
