import os

from django.contrib.gis.utils import LayerMapping

from livinglots_lots.exceptions import ParcelAlreadyInLot
from livinglots_lots.models import Use
from lots.models import Lot
from owners.models import Owner
from ..load import get_processed_data_file
from ..parcels.models import Parcel
from .models import WaterfrontParcel, waterfront_parcel_mapping


def load(**kwargs):
    from_shapefile(**kwargs)


def from_shapefile(strict=True, progress=True, verbose=False, **kwargs):
    """
    Load waterfront data into the database from the processed shapefile.
    """
    shp = get_processed_data_file(os.path.join('waterfront', 'waterfront.shp'))
    mapping = LayerMapping(WaterfrontParcel, shp, waterfront_parcel_mapping, transform=False)
    mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)

    use = Use.objects.get_or_create(
        name='waterfront',
        visible=True,
    )[0]

    # Add parcel to waterfrontparcel
    for waterfront_parcel in WaterfrontParcel.objects.all():
        # Don't add parcels that are under Parks jurisdiction
        if waterfront_parcel.ownerfixed == 'New York City Department of Parks and Recreation':
            continue
        parcel = None
        if waterfront_parcel.bbl:
            try:
                parcel = Parcel.objects.with_bbl(bbl=waterfront_parcel.bbl)[0]
            except Exception:
                pass
        if not parcel:
            try:
                parcel = Parcel.objects.get(geom__contains=waterfront_parcel.geom)
            except Exception:
                pass
        if parcel:
            waterfront_parcel.parcel = parcel
            waterfront_parcel.save()

            try:
                lot_kwargs = {
                    'added_reason': 'Loaded with waterfront data',
                    'commons_content_object': waterfront_parcel,
                    'commons_type': 'waterfront',
                    'country': 'USA',
                    'known_use': use,
                    'known_use_certainty': 8,
                    'known_use_locked': True,
                    'owner_opt_in': True,
                    'state_province': 'NY',
                }
                lot = Lot.objects.create_lot_for_parcel(parcel, **lot_kwargs)

                if waterfront_parcel.ownerfixed:
                    # Don't trust owner from MapPLUTO, use the one in the download
                    (owner, created) = Owner.objects.get_or_create(
                        name=waterfront_parcel.ownerfixed,
                        defaults={
                            'owner_type': 'public',
                        },
                        ignorecase=False
                    )
                    lot.owner = owner
                    lot.save()
                else:
                    print 'could not find ownerfixed, using', lot.owner.name
            except ParcelAlreadyInLot:
                print '\tParcel %s already in a lot. Skipping.' % parcel
                continue
