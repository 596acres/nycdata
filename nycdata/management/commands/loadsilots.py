"""
Load vacant lots in Staten Island found by Pratt SAVI in December 2014.

"""
from optparse import make_option

import fiona

from django.core.management.base import BaseCommand

from livinglots_lots.exceptions import ParcelAlreadyInLot
from lots.models import Lot
from ...parcels.models import Parcel


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads vacant lots in Staten Island found by Pratt SAVI'

    option_list = BaseCommand.option_list + (
        make_option('--do-over',
            action='store',
            dest='do_over',
            default=False,
            help='Attempt to undo a previous load.',
            metavar='DATETIME',
       ),
    )

    lot_kwargs = {
        'added_reason': 'Imported from Pratt SAVI work',
        'country': 'USA',
        'known_use': None,
        'known_use_certainty': 10,
        'known_use_locked': True,
        'state_province': 'NY',
    }

    def handle(self, filename, *args, **options):
        if options['do_over']:
            print 'Deleting everything added after %s' % options['do_over']
            print 'Deleting Lot instances.'
            Lot.objects.filter(added__gte=options['do_over']).delete()
        self.load_si_lots(fiona.open(filename))

    def load_si_lots(self, shp):
        for feature in shp:
            self.load_si_lot(feature)

    def load_si_lot(self, feature):
        """Create a lot using a feature from the SAVI shapefile."""
        properties = feature['properties']
        parcels = Parcel.objects.with_bbl(
            borough='Staten Island',
            block=properties['Block'],
            lot=properties['Lot']
        )
        if not parcels.exists():
            print '***\n***\n*** No Parcels found for %s. Skipping.\n***\n***' % feature
            return
        if len(parcels) > 1:
            print '***\n***\n*** Too many Parcels found for %s. Skipping.\n***\n***' % feature
            return
        parcel = parcels[0]
        kwargs = dict(self.lot_kwargs)

        print 'Adding %s' % parcel

        # Check notes column for gutterspaceness
        if properties['Notes'] == 'GUTTER SPACE' or properties['Type'] == 'GUTTER SPACE':
            kwargs['gutterspace'] = True

        try:
            lot = Lot.objects.create_lot_for_parcel(parcel, **kwargs)
        except ParcelAlreadyInLot:
            print '\tParcel %s already in a lot. Skipping.' % parcel
            return

        print '\tMaking %s public' % lot.owner
        # Force owner to be public
        lot.owner.owner_type = 'public'
        lot.owner.save()
