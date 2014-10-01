#
# Load owner contacts (non-default) exported from original database
#
import csv

from django.core.management.base import BaseCommand

from lots.models import Lot
from owners.models import OwnerContact


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC owner contacts exported from original database'

    def get_owner_contact(self, owner=None, name=None, **defaults):
        defaults = { k: defaults[k] for k in ('phone', 'email', 'notes') }
        return OwnerContact.objects.get_or_create(name=name, owner=owner,
                                                  defaults=defaults)[0]

    def load_ownercontacts(self, ownercontacts_file):
        for row in csv.DictReader(ownercontacts_file):
            try:
                lot = Lot.objects.get(bbl=row['bbl'])
                print row
                lot.owner_contact = self.get_owner_contact(owner=lot.owner, **row)
                lot.save()
            except Lot.DoesNotExist:
                continue

    def handle(self, filename, *args, **options):
        self.load_ownercontacts(open(filename, 'r'))
