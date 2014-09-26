#
# Load organizers exported from original database
#
import csv

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from livinglots_organize.models import OrganizerType
from lots.models import Lot
from organize.models import Organizer


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
        defaults['post_publicly'] = True
        organizer = Organizer.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(lot),
            object_id=lot.pk,
            name=kwargs['name'],
            type=type,
            defaults=defaults,
        )[0]

        Organizer.objects.filter(pk=organizer.pk).update(added=added)
        return organizer

    def load_organizers(self, organizers_file):
        for row in csv.DictReader(organizers_file):
            print row
            try:
                lot = Lot.objects.get(bbl=row['bbl'])
                self.add_organizer(lot, **row)
            except Lot.DoesNotExist:
                print "Couldn't find lot, skipping"
                continue

    def handle(self, filename, *args, **options):
        self.load_organizers(open(filename, 'r'))
