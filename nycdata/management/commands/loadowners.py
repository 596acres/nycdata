#
# Load owners exported from original database
#
import csv

from django.core.management.base import BaseCommand

from lots.models import Lot
from owners.models import Owner, OwnerContact


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC owners exported from original database'

    def get_owner_contact(self, owner=None, name=None, **defaults):
        try:
            defaults = { k: defaults[k] for k in ('phone', 'email', 'notes') }
            return OwnerContact.objects.get_or_create(name=name, owner=owner,
                                                      defaults=defaults)[0]
        except Exception:
            return None

    def get_owner(self, name=None, type=None, **kwargs):
        try:
            if type == 'city':
                type = 'public'
            else:
                type = 'private'
            return Owner.objects.get_or_create(name=name, defaults={
                'owner_type': type,
            })[0]
        except Exception:
            return None

    def load_owners(self, owners_file):
        for row in csv.DictReader(owners_file):
            try:
                lot = Lot.objects.get(bbl=row['bbl'])
                print row
                lot.owner = self.get_owner(**row)
                lot.owner_contact = self.get_owner_contact(**row)
                lot.save()
            except Lot.DoesNotExist:
                continue

    def handle(self, filename, *args, **options):
        self.load_owners(open(filename, 'r'))
