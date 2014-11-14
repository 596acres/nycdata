#
# Load owners and default owner contacts exported from original database
#
import csv

from django.core.management.base import BaseCommand
from django.db.models import Count

from lots.models import Lot
from owners.models import Owner, OwnerContact

from nycdata.imports.utils import get_lot


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC owners exported from original database'
    private_opted_in_owners = ('New York City Transit (MTA)',)

    def get_owner_contact(self, owner=None, site=None, **kwargs):
        defaults = { k: kwargs[k] for k in ('phone', 'email', 'notes') }
        defaults['url'] = site
        try:
            return OwnerContact.objects.get_or_create(
                name=kwargs['person'] or owner.name,
                owner=owner,
                defaults=defaults
            )[0]
        except ValueError:
            return None

    def get_owner(self, name=None, type=None, **kwargs):
        try:
            if type == 'city':
                type = 'public'
            else:
                type = 'private'
            if name in self.private_opted_in_owners:
                type = 'private'
            return Owner.objects.get_or_create(name=name, defaults={
                'owner_type': type,
            })[0]
        except Exception:
            return None

    def load_owners(self, owners_file):
        for row in csv.DictReader(owners_file):
            try:
                lot = get_lot(row['bbl'])
                print row
                lot.owner = self.get_owner(**row)
                lot.owner_contact = self.get_owner_contact(owner=lot.owner, **row)
                if not lot.known_use and lot.owner.name in self.private_opted_in_owners:
                    lot.owner_opt_in = True
                lot.save()
            except Lot.DoesNotExist:
                continue

    def make_default_owner_contacts(self):
        for owner in Owner.objects.all():
            most_used_contact = Lot.objects.filter(owner=owner) \
                    .values('owner_contact__pk') \
                    .annotate(oc_count=Count('pk')) \
                    .order_by('oc_count')[0]['owner_contact__pk']
            owner.default_contact = OwnerContact.objects.get(pk=most_used_contact)
            owner.save()

    def handle(self, filename, *args, **options):
        print '\n\nLoading owners...'
        self.load_owners(open(filename, 'r'))
        print '\n\nCreating default ownercontacts...'
        self.make_default_owner_contacts()
