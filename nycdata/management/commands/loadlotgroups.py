#
# Load lot groups exported from original database
#
import csv

from django.core.management.base import BaseCommand

from lots.models import Lot, LotGroup


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC lot groups exported from original database'

    def load_lot_groups(self, lot_groups_file):
        for row in csv.DictReader(lot_groups_file):
            print row
            try:
                lot = Lot.objects.get(bbl=row['bbl'])
                parent_lot = Lot.objects.get(bbl=row['parent'])
            except Lot.DoesNotExist:
                print "Couldn't find lot, skipping"
                continue

            try:
                # Try to get parent lot's lotgroup, add to that
                lot_group = LotGroup.objects.get(lot=parent_lot)
                lot_group.add(lot)
            except Lot.DoesNotExist:
                # Else create a lotgroup, add both to it
                lot_group = LotGroup(**{
                    'address_line1': parent_lot.address_line1,
                    'borough': parent_lot.borough,
                    'known_use': parent_lot.known_use,
                    'name': parent_lot.name,
                    'postal_code': parent_lot.postal_code,
                })
                lot_group.save()
                lot_group.update(lots=(parent_lot, lot))

                # Assume previous lot had the group's name, not its own name.
                # Delete since the group now has it.
                parent_lot.name = None
                parent_lot.save()

    def handle(self, filename, *args, **options):
        self.load_lot_groups(open(filename, 'r'))
