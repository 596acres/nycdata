#
# Load organizers exported from original database
#
import csv

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from livinglots_organize.models import OrganizerType
from lots.models import Lot
from organize.models import Organizer

from nycdata.imports.utils import get_lot


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC organizers exported from original database'

    def add_organizer(self, lot, added=None, **kwargs):
        type = OrganizerType.objects.get_or_create(
            name=kwargs['type'],
            is_group=kwargs['is_group'],
        )[0]

        organizer_fields = ('phone', 'email', 'email_hash', 'notes', 'url',
                            'notes', 'facebook_page',)
        defaults = { k: kwargs[k] for k in organizer_fields }
        organizer = Organizer.objects.get_or_create(
            # Explicitly add to the Lot object rather than the LotGroup
            content_type=ContentType.objects.get_for_model(Lot),
            object_id=lot.pk,
            name=kwargs['name'],
            post_publicly=True,
            type=type,
            defaults=defaults,
        )[0]

        Organizer.objects.filter(pk=organizer.pk).update(added=added)
        return organizer

    def load_organizers(self, organizers_file):
        for row in csv.DictReader(organizers_file):
            print row
            try:
                lot = get_lot(row['bbl'])
                self.add_organizer(lot, **row)
            except Lot.DoesNotExist:
                print "Couldn't find lot, skipping"
                continue

    def handle(self, filename, *args, **options):
        self.load_organizers(open(filename, 'r'))
