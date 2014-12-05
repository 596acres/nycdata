#
# Load pictures exported from original database
#
import csv
import os
import subprocess

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from livinglots_usercontent.photos.models import Photo
from lots.models import Lot

from nycdata.imports.utils import get_lot


class Command(BaseCommand):
    args = 'pictures_csv pictures_archive'
    help = 'Loads NYC pictures exported from original database'

    def load_pictures(self, pictures_file):
        for row in csv.DictReader(pictures_file):
            print row
            try:
                lot = get_lot(row['bbl'])
                fields = {
                    'content_type': ContentType.objects.get_for_model(Lot),
                    'object_id': lot.pk,
                    'description': row['description'],
                    # These used to be stored under pictures, let's fix that
                    # here.
                    'original_image': row['picture'].replace('pictures',
                                                             'photos', 1),
                }
                photo = Photo(**fields)
                photo.save()

                photo.action_object_actions.update(timestamp=row['added'])
                Photo.objects.filter(pk=photo.pk).update(added=row['added'])
            except Lot.DoesNotExist:
                print "Couldn't find lot, skipping"
                continue

    def move_picture_files(self, pictures_archive):
        pictures_dir = os.path.join(settings.MEDIA_ROOT, 'photos')

        # Make directory for the pictures
        try:
            os.mkdir(pictures_dir)
        except OSError:
            # Directory already exists, move along
            pass

        # Untar into our new pictures directory
        untar_cmd = 'tar -xf %s -C %s' % (
            os.path.abspath(pictures_archive),
            os.path.abspath(pictures_dir)
        )
        print untar_cmd
        subprocess.call(untar_cmd, shell=True)

    def handle(self, filename, archive_filename, *args, **options):
        #self.load_pictures(open(filename, 'r'))
        self.move_picture_files(archive_filename)
