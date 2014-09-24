#
# Load lots exported from original database
#
import csv

from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from livinglots_lots.models import Use
from lots.models import Lot


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC lots exported from original database'

    def get_centroid(self, wkt):
        try:
            return GEOSGeometry('SRID=4326;' + wkt)
        except (TypeError, ValueError):
            return None

    def get_use(self, name):
        try:
            return Use.objects.get_or_create(name=name)[0]
        except Exception:
            return None

    def load_lots(self, lots_file):
        lots = csv.DictReader(lots_file)

        for lot in lots:
            newlot = Lot(
                address_line1=lot['address'],
                borough=lot['borough'],
                bbl=lot['bbl'],
                block=lot['block'],
                lot=lot['lot'],
                state_province='NY',
                country='USA',
                postal_code=lot['zipcode'],
                centroid=self.get_centroid(lot['centroid']),
                known_use=self.get_use(lot['actual_use']),
                accessible=lot['accessible'] == 't',
                name=lot['name'],
            )
            newlot.save()

    def handle(self, filename, *args, **options):
        self.load_lots(open(filename, 'r'))
