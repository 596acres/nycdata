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
                lot_group = LotGroup(**Lot.objects.filter(pk=parent_lot.pk).values()[0])
                lot_group.save()
                lot_group.add(lot)
                lot_group.add(parent_lot)

    def handle(self, filename, *args, **options):
        self.load_lot_groups(open(filename, 'r'))
