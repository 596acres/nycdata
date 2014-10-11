#
# Load owner contacts (non-default) exported from original database
#
import csv

from django.core.management.base import BaseCommand

from lots.models import Lot
from owners.models import OwnerContact

from nycdata.imports.utils import get_lot


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
                lot = get_lot(row['bbl'])
                #print row
                lot.owner_contact = self.get_owner_contact(owner=lot.owner, **row)
                lot.save()
            except Lot.DoesNotExist:
                print '*** Could not find lot %s' % row['bbl']
                continue
            except Exception:
                print '*** Error adding %s' % row['bbl']
                import traceback
                traceback.print_exc()

    def handle(self, filename, *args, **options):
        print '\n\nLoading ownercontacts...'
        self.load_ownercontacts(open(filename, 'r'))
