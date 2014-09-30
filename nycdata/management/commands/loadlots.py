#
# Load lots exported from original database
#
import csv

from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from livinglots_lots.models import Use
from lots.models import Lot
from nycdata.parcels.models import Parcel


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC lots exported from original database'

    def get_centroid(self, wkt):
        try:
            return GEOSGeometry('SRID=4326;' + wkt)
        except (TypeError, ValueError):
            return None

    def get_use(self, name):
        if not name:
            return None
        try:
            return Use.objects.get_or_create(
                name=name,
                visible=False,
            )[0]
        except Exception:
            return None

    def get_parcel(self, bbl=None, centroid=None, **kwargs):
        # TODO try to get by geom, then get by bbl
        try:
            return Parcel.objects.get(geom__contains=centroid)
        except Parcel.MultipleObjectsReturned:
            return Parcel.objects.get(geom__contains=centroid, bbl=bbl)
        except (ValueError, Parcel.DoesNotExist):
            return Parcel.objects.get(bbl=bbl)

    def load_lots(self, lots_file):
        lots = csv.DictReader(lots_file)

        for lot in lots:
            centroid = self.get_centroid(lot['centroid'])
            parcel = None
            polygon = None

            if not centroid:
                continue

            try:
                parcel = self.get_parcel(centroid=centroid, bbl=lot['bbl'])
                polygon = parcel.geom
            except Parcel.DoesNotExist:
                print "No parcel for lot %s. That's okay, adding." % lot['bbl']
            except Parcel.MultipleObjectsReturned:
                print '* TOO MANY Parcels returned for lot %s. Skipping.' % lot['bbl']
                continue
            except ValueError:
                print '* No bbl or centroid for lot %s. Skipping.' % lot['bbl']
                continue

            newlot = Lot(
                address_line1=lot['address'],
                borough=lot['borough'],
                bbl=lot['bbl'],
                block=lot['block'],
                lot_number=lot['lot'],
                state_province='NY',
                country='USA',
                postal_code=lot['zipcode'],
                centroid=self.get_centroid(lot['centroid']),
                polygon=polygon,
                known_use=self.get_use(lot['actual_use']),
                known_use_certainty=9,
                known_use_locked=True,
                accessible=lot['accessible'] == 't',
                name=lot['name'],
                parcel=parcel,
            )
            newlot.save()

    def handle(self, filename, *args, **options):
        self.load_lots(open(filename, 'r'))
