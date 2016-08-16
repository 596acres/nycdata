import os

from django.contrib.gis.utils import LayerMapping

from livinglots_lots.exceptions import ParcelAlreadyInLot
from livinglots_lots.models import Use
from lots.models import Lot
from owners.models import Owner
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

    use = Use.objects.get_or_create(
        name='post office',
        visible=True,
    )[0]

    # Add parcel to post office
    for post_office in PostOffice.objects.filter(public='yes'):
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
            # Delete any waterfront lots
            parcel.lot_set.filter(commons_type='waterfront').delete()

            post_office.parcel = parcel
            post_office.save()

            try:
                post_office_name = post_office.name
                if 'post office' not in post_office_name.lower():
                    post_office_name += ' Post Office'
                lot_kwargs = {
                    'added_reason': 'Loaded with post office data',
                    'city': post_office.city,
                    'commons_content_object': post_office,
                    'commons_type': 'post office',
                    'country': 'USA',
                    'name': post_office_name,
                    'known_use': use,
                    'known_use_certainty': 8,
                    'known_use_locked': True,
                    'owner_opt_in': True,
                    'state_province': 'NY',
                }
                lot = Lot.objects.create_lot_for_parcel(parcel, **lot_kwargs)

                if post_office.ownerfixed:
                    # Don't trust owner from MapPLUTO, use the one in the download
                    (owner, created) = Owner.objects.get_or_create(
                        name=post_office.ownerfixed,
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
