#
# Load lots exported from original database
#
import csv

from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from livinglots_lots.models import Use
from lots.models import Lot, LotGroup
from nycdata.parcels.models import Parcel
from steward.models import StewardProject


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads NYC lots exported from original database'

    def get_centroid(self, wkt):
        try:
            return GEOSGeometry('SRID=4326;' + wkt)
        except (TypeError, ValueError):
            return None

    def get_use(self, actual_use=None, accessible='t', is_vacant='t', **kwargs):
        visible = False
        if not actual_use and not is_vacant == 't':
            actual_use = 'generic use: not vacant'
        if not actual_use:
            return None
        if actual_use.startswith('Garden'):
            actual_use = 'community garden'
            visible = True

        # Gutterspace
        if not actual_use and not accessible == 't':
            return None
        if actual_use.lower().startswith('gutterspace'):
            return None

        try:
            return Use.objects.get_or_create(
                name=actual_use,
                visible=visible,
            )[0]
        except Exception:
            return None

    def get_name(self, actual_use=None, name=None, **kwargs):
        if actual_use.startswith('Garden'):
            return actual_use.split('|')[1]
        return name

    def get_parcel(self, bbl=None, centroid=None, **kwargs):
        """
        Try to get a parcel by BBL, otherwise get it by centroid.
        """
        try:
            return Parcel.objects.get(bbl=bbl)
        except Parcel.DoesNotExist:
            return Parcel.objects.get(geom__contains=centroid)
        except Parcel.MultipleObjectsReturned:
            return Parcel.objects.get(geom__contains=centroid, bbl=bbl)

    def add_steward_project(self, lot, actual_use=None):
        """
        Add steward project to lot if it is a garden that's being imported.
        """
        use, name, external_id = actual_use.split('|')
        unique_kwargs = {
            'project_name': name,
            'external_id': external_id,
        }
        defaults = {
            'include_on_map': True,
            'started_here': False,
            'use': lot.known_use,
        }
        type_kwargs = {
            'content_type': ContentType.objects.get_for_model(lot),
            'object_id': lot.pk,
        }

        # If we don't have a name to make the project unique, add lot id
        if not name:
            unique_kwargs.update(**type_kwargs)
        else:
            defaults.update(**type_kwargs)

        steward_project, created = StewardProject.objects.get_or_create(
            defaults=defaults,
            **unique_kwargs
        )

        # If the project already existed let's add this lot to the project
        if not created:
            parent_lot = steward_project.content_object
            try:
                # Try to get parent lot's lotgroup and add to that
                lot_group = parent_lot.lotgroup
                lot_group.add(lot)
            except Lot.DoesNotExist:
                # Else create a lotgroup, add both to it
                lot_group = LotGroup(**{
                    'address_line1': parent_lot.address_line1,
                    'borough': parent_lot.borough,
                    'known_use': parent_lot.known_use,
                    'name': parent_lot.name,
                    'postal_code': parent_lot.postal_code,
                })
                lot_group.save()
                lot_group.update(lots=(parent_lot, lot))

                # Update the object for this project
                steward_project.content_object = lot_group
                steward_project.save()
        lot.steward_inclusion_opt_in = True
        lot.save()

    def load_lots(self, lots_file):
        lots = csv.DictReader(lots_file)

        for lot in lots:
            actual_use = lot['actual_use']
            centroid = self.get_centroid(lot['centroid'])
            parcel = None
            polygon = None
            gutterspace = False

            if not centroid:
                continue

            if not actual_use and not lot['accessible'] == 't':
                gutterspace = True
            if actual_use.lower().startswith('gutterspace'):
                gutterspace = True

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
                known_use=self.get_use(**lot),
                known_use_certainty=9,
                known_use_locked=True,
                accessible=lot['accessible'] == 't',
                name=self.get_name(**lot),
                parcel=parcel,
                added_reason='Imported from 596 Acres Classic',
                gutterspace=gutterspace,
            )
            newlot.save()

            if actual_use.startswith('Garden'):
                try:
                    self.add_steward_project(newlot, actual_use=lot['actual_use'])
                except ValueError:
                    print "Couldn't add steward project for lot:", newlot, actual_use
                    continue

    def handle(self, filename, *args, **options):
        self.load_lots(open(filename, 'r'))
