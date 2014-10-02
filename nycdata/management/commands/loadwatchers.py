#
# Load watchers exported from original database
#
import csv

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from livinglots_organize.models import OrganizerType
from lots.models import Lot, LotGroup
from organize.models import Organizer


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC watchers exported from original database'

    def add_watcher(self, lot, added=None, **kwargs):
        # assume individual
        type = OrganizerType.objects.get_or_create(name='individual', is_group=False)[0]

        fields = ('phone', 'email', 'email_hash',)
        defaults = { k: kwargs[k] for k in fields }
        organizer = Organizer.objects.get_or_create(
            # Explicitly add to the Lot object rather than the LotGroup
            content_type=ContentType.objects.get_for_model(Lot),
            object_id=lot.pk,
            name=kwargs['name'],
            post_publicly=False,
            type=type,
            defaults=defaults,
        )[0]

        Organizer.objects.filter(pk=organizer.pk).update(added=added)
        return organizer

    def load_watchers(self, watchers_file):
        for row in csv.DictReader(watchers_file):
            print row
            try:
                try:
                    lot = LotGroup.objects.get(lot__bbl=row['bbl'])
                except LotGroup.DoesNotExist:
                    lot = Lot.objects.get(bbl=row['bbl'])
                self.add_watcher(lot, **row)
            except Lot.DoesNotExist:
                print "Couldn't find lot, skipping"
                continue

    def handle(self, filename, *args, **options):
        self.load_watchers(open(filename, 'r'))
