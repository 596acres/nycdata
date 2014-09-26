#
# Load notes exported from original database
#
import csv

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from livinglots_usercontent.notes.models import Note
from lots.models import Lot


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC notes exported from original database'

    def load_notes(self, notes_file):
        for row in csv.DictReader(notes_file):
            print row
            try:
                lot = Lot.objects.get(bbl=row['bbl'])
                fields = {
                    'content_type': ContentType.objects.get_for_model(lot),
                    'object_id': lot.pk,
                    'text': row['text'],
                    'added_by_name': row['added_by_name'],
                }
                note = Note(**fields)
                note.save()

                Note.objects.filter(pk=note.pk).update(added=row['added'])
            except Lot.DoesNotExist:
                print "Couldn't find lot, skipping"
                continue

    def handle(self, filename, *args, **options):
        self.load_notes(open(filename, 'r'))
