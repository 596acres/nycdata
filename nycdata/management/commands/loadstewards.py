#
# Load stewards exported from original database
#
import csv

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from livinglots_lots.models import Use
from livinglots_organize.models import OrganizerType
from lots.models import Lot
from organize.models import Organizer
from steward.models import StewardProject

from nycdata.imports.utils import get_lot


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC stewards exported from original database'

    def get_organizer(self, lot, added=None, **kwargs):
        type = OrganizerType.objects.get_or_create(
            name=kwargs['type'],
            is_group=kwargs['is_group'] == 't',
        )[0]

        organizer_fields = ('phone', 'email', 'email_hash', 'notes', 'url',
                            'notes', 'facebook_page',)
        defaults = { k: kwargs[k] for k in organizer_fields }
        defaults['post_publicly'] = True
        organizer = Organizer.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(Lot),
            object_id=lot.pk,
            name=kwargs['name'],
            type=type,
            defaults=defaults,
        )[0]

        Organizer.objects.filter(pk=organizer.pk).update(added=added)
        return organizer

    def get_use(self):
        return Use.objects.get_or_create(
            name='community green space',
            visible=True,
        )[0]

    def add_steward_project(self, lot, **kwargs):
        defaults = {
            'include_on_map': True,
            'started_here': True,
            'use': self.get_use(),
        }
        return StewardProject.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(lot),
            object_id=lot.pk,
            project_name=kwargs['name'],
            organizer=self.get_organizer(lot, **kwargs),
            defaults=defaults,
        )[0]

    def load_stewards(self, steward_file):
        for row in csv.DictReader(steward_file):
            print row
            try:
                lot = get_lot(row['bbl'])
                lot.known_use = self.get_use()
                lot.known_use_certainty = 10
                lot.known_use_locked = True
                lot.steward_inclusion_opt_in = True
                lot.save()
                self.add_steward_project(lot, **row)
            except Lot.DoesNotExist:
                print "Couldn't find lot, skipping"
                continue

    def handle(self, filename, *args, **options):
        self.load_stewards(open(filename, 'r'))
