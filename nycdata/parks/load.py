import os

from django.contrib.gis.db.models.functions import Area, Intersection, Transform
from django.contrib.gis.utils import LayerMapping

from livinglots_lots.exceptions import ParcelAlreadyInLot
from livinglots_lots.models import Use
from lots.models import Lot
from owners.models import Owner
from ..load import get_processed_data_file
from ..parcels.models import Parcel
from .models import Park, park_mapping


def load(**kwargs):
    from_shapefile(**kwargs)


def from_shapefile(strict=True, progress=True, verbose=False, **kwargs):
    """
    Load park data into the database from the processed shapefile.
    """
    shp = get_processed_data_file(os.path.join('parks', 'parks.shp'))
    mapping = LayerMapping(Park, shp, park_mapping, transform=False)
    mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)

    owner = Owner.objects.get_or_create(
        'New York City Department of Parks and Recreation',
        defaults={ 'owner_type': 'public',}
    )[0]
    use = Use.objects.get_or_create(
        name='park',
        visible=True,
    )[0]

    for park in Park.objects.exclude(typecatego='Garden'):
        try:
            create_lot_for_park(park, use, owner)
        except Exception as e:
            print 'Exception getting parcels for park %s. Skipping.' % park.signname
            print e
            continue


def create_lot_for_park(park, use, default_owner):
    lot_kwargs = {
        'added_reason': 'Loaded with park data',
        'commons_content_object': park,
        'commons_type': 'park',
        'country': 'USA',
        'name': park.signname,
        'known_use': use,
        'known_use_certainty': 8,
        'known_use_locked': True,
        'owner_opt_in': True,
        'state_province': 'NY',
    }
    if lot_kwargs['name'] in ('Triangle', 'Park',):
        lot_kwargs['name'] = None

    parcels = []
    matching_parcels = Parcel.objects.filter(geom__overlaps=park.geom).annotate(
        intersect_area=Area(Transform(Intersection('geom', park.geom), 2263)),
        geom_area=Area(Transform('geom', 2263))
    )
    parcels = [p for p in matching_parcels if p.intersect_area.sq_ft > p.geom_area.sq_ft * .9]
    parcels = [p for p in parcels if not p.lot_set.exists()]

    lot = None
    if parcels:
        # Delete any waterfront lots
        for parcel in parcels:
            parcel.lot_set.filter(commons_type='waterfront').delete()

        lot = Lot.objects.create_lot_for_parcels(parcels, allow_overlap=True, **lot_kwargs)
    else:
        # Make up fake parcels for property not on a parcel (eg parkways)
        lot = Lot.objects.create_lot_for_geom(park.geom, **lot_kwargs)

    # If owner is null update to parks
    if lot and not lot.owner:
        lot.owner = default_owner
        lot.save()
