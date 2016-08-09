import os

from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.utils import LayerMapping

from livinglots_lots.models import Use
from lots.models import Lot
from owners.models import Owner
from ..load import get_processed_data_file
from ..parcels.models import Parcel
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
    owner = Owner.objects.get_or_create(
        name='NYCHA',
        defaults={ 'owner_type': 'public' },
    )[0]
    use = Use.objects.get_or_create(
        name='public housing',
        visible=True,
    )[0]

    for nycha_development in NYCHADevelopment.objects.all():
        print 'Adding lot for NYCHA development %s' % nycha_development.name

        lot_kwargs = {
            'added_reason': 'Loaded with NYCHA data',
            'borough': nycha_development.borough.title(),
            'city': nycha_development.borough.title(),
            'commons_content_object': nycha_development,
            'commons_type': 'public housing',
            'country': 'USA',
            'name': nycha_development.name,
            'known_use': use,
            'known_use_certainty': 8,
            'known_use_locked': True,
            'owner': owner,
            'state_province': 'NY',
        }

        # NB: NYCHA developments often span multiple parcels or portions of
        # parcels, so we add them as drawn geometries here rather than tie them
        # to particular parcels.

        # Some NYCHA developments span multiple small houses spread over various
        # boroughs. Here we create separate lots for them since we are more 
        # likely to think of them in terms of an individual home than the entire
        # development. The development will still be available as the
        # commons_content_object.
        if nycha_development.borough == 'VARIOUS':
            del lot_kwargs['borough']
            del lot_kwargs['city']
            for geom in nycha_development.geom:
                # Try to add each part of a split development as its parcel
                try:
                    parcel = Parcel.objects.get(geom__contains=geom.centroid)
                    lot_kwargs_copy = lot_kwargs.copy()
                    del lot_kwargs_copy['name']
                    lot = Lot.objects.create_lot_for_parcel(parcel,
                            **lot_kwargs_copy)
                    lot.owner = owner
                    lot.name = '%s: %s' % (
                        nycha_development.name,
                        lot.address_line1,
                    )
                    lot.save()
                except Exception, e:
                    Lot.objects.create_lot_for_geom(MultiPolygon(geom), **lot_kwargs)
        else:
            Lot.objects.create_lot_for_geom(nycha_development.geom, **lot_kwargs)
