"""
Load community gardens from the latest GrowNYC database of community gardens in
NYC.

"""
import csv
from datetime import date
import json
import itertools
from optparse import make_option

from dateutil.parser import parse
import fiona

from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from livinglots_lots.models import Use
from livinglots_organize.models import OrganizerType

from lots.models import Lot, LotGroup
from organize.models import Organizer
from owners.models import Owner
from steward.models import StewardProject

from ...bbls import build_bbl
from ...bbls.build import get_int
from ...boroughs import borough_number
from ...parcels.models import Parcel


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads community gardens from GrowNYC database'
    option_list = BaseCommand.option_list + (
        make_option('--do-over',
            action='store',
            dest='do_over',
            default=False,
            help='Attempt to undo a previous load.',
            metavar='DATETIME',
       ),

        make_option('--shp',
            action='store',
            dest='shp',
            default=None,
            help='A shapefile of community gardens',
            metavar='SHP',
        )
    )

    lot_kwargs = {
        'added_reason': 'Imported from GrowNYC database',
        'country': 'USA',
        'known_use_certainty': 8,
        'known_use_locked': True,
        'owner_opt_in': True,
        'state_province': 'NY',
        'steward_inclusion_opt_in': True,
    }

    def handle(self, filename, *args, **options):
        if options['do_over']:
            print 'Deleting everything added after %s' % options['do_over']
            # NB: Owner instances are not handled here
            for model in (Organizer, LotGroup, Lot):
                print 'Deleting %s instances.' % model
                model.objects.filter(added__gte=options['do_over']).delete()
            print 'Deleting StewardProject orphans'
            for project in StewardProject.objects.all():
                if project.content_object is None:
                    project.delete()
        else:
            shp = None
            if options['shp']:
                shp = self.open_gardens_shapefile(options['shp'])
            self.load_community_gardens(open(filename, 'r'), shp=shp)

    def load_community_gardens(self, infile, shp=None):
        rows = csv.DictReader(infile)
        rows = sorted(rows, key=lambda r: r['Community Garden'].strip())
        gardens = itertools.groupby(rows, lambda r: r['Community Garden'].strip())

        owners_out = csv.DictWriter(open('loadgardens_owners_compare.csv', 'w'),
                                    ['bbl', 'LLNYC owner', 'GrowNYC owner'])
        owners_out.writeheader()

        results_out = csv.DictWriter(open('loadgardens_results.csv', 'w'), [
            'name',
            'created lots',
            'created lotgroup',
            'created stewardproject',
            'existing project',
            'parcels missing',
            'parcels imported',
        ])
        results_out.writeheader()

        for garden_name, garden_parcels in gardens:
            # Skip schools
            if garden_name.startswith('P.S.') or garden_name.startswith('M.S.'):
                continue

            garden_parcels = list(garden_parcels)
            self.add_community_garden(garden_name, garden_parcels, results_out,
                                      owners_out, shp=shp)

    def add_community_garden(self, garden_name, garden_parcels, results_out,
                             owners_out, shp=None):
        """
        Add a community garden from the GrowNYC data.

        First we test whether the parcels involved are already in the database.
        If so, and they make up a project facilitated through 596 Acres, we skip
        them (assuming we have more accurate data for those).

        Then we create lots for any BBLs listed that we can find as parcels
        (meaning they are in PLUTO).

        If we still have no lots at this point, we refer back to the GrowNYC
        shapefile and try to find the garden's shape based on the gardenid
        field.

        Finally, we create a StewardProject instance for the lot or group of
        lots.
        """
        print garden_name

        results = {
            'name': garden_name,
            'created lots': False,
            'created lotgroup': False,
            'created stewardproject': False,
            'existing project':  self.find_existing_project(garden_parcels),
            'parcels missing': False,
            'parcels imported': False,
        }

        # Check for existing steward project immediately, don't add anything
        if results['existing project']:
            results_out.writerow(results)
            return

        lots = []
        for garden_parcel in garden_parcels:
            bbl = build_bbl(garden_parcel['Boro'], garden_parcel['Block'],
                            garden_parcel['Lot'])
            try:
                parcel = Parcel.objects.get(bbl=bbl)
            except Parcel.DoesNotExist:
                print '\tCould not find %s' % bbl
                results['parcels missing'] = True
                continue

            lot, created = self.get_or_create_lot(bbl, parcel, garden_parcel)
            lots.append(lot)

            if created:
                results['created lots'] = True

            # Write owners out to a CSV for later review
            owners_out.writerow({ 
                'bbl': bbl,
                'LLNYC owner': lot.owner,
                'GrowNYC owner': garden_parcel['descrip_TYPE'],
            })

        # If we can't find lots in Parcels (PLUTO), try the shapefile
        if shp and not lots:
            print '\tNo lots found, trying from shp.'
            shp_parcel = self.find_in_shapefile(shp, garden_parcels[0]['GARDENID'])
            if not shp_parcel:
                print '\t\tCould not find garden in shapefile--skipping.'
            else:
                lot = self.create_lot_from_shp(shp_parcel, garden_parcels[0])
                lots = [lot,]
                print '\t\tFound garden in shapefile--adding.'
                results['parcels imported'] = True

        if not lots:
            print '\tNo lots found, not adding.'
            return

        if len(lots) > 1:
            lot, results['created lotgroup'] = self.get_or_create_lotgroup(lots)

        # No matter what, rename the lot
        lot.name = garden_name
        lot.save()

        # Create steward project if doesn't exist
        if not lot.steward_projects.exists():
            results['created stewardproject'] = True
            self.add_steward_project(lot, garden_parcel, name=garden_name)

        results_out.writerow(results)

    
    #
    # Get / create model instances
    #
    def find_existing_project(self, rows):
        for row in rows:
            bbl = build_bbl(row['Boro'], row['Block'], row['Lot'])
            if not bbl:
                continue
            for lot in Lot.objects.filter(bbl=bbl):
                if StewardProject.objects.filter(
                    content_type=ContentType.objects.get_for_model(Lot),
                    object_id=lot.pk,
                    started_here=True,
                ).exists():
                    return True
        return False

    def add_steward_project(self, lot, row, **kwargs):
        defaults = {
            'include_on_map': True,
            'started_here': False,
            'use': self.get_use(),
        }

        # Attempt to get the date started
        date_started = None
        try:
            date_started = parse(row['Year Founded'], fuzzy=True,
                                 default=date(1, 1, 1))
            if date_started.year == 1:
                date_started = None
        except ValueError:
            pass

        return StewardProject.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(Lot),
            object_id=lot.pk,
            project_name=kwargs['name'],
            organizer=self.get_organizer(lot, row, **kwargs),
            external_id=row['GARDENID'],
            support_organization=row['ORGANIZATION'],
            date_started=date_started,
            defaults=defaults,
        )[0]

    def get_or_create_lotgroup(self, lots):
        """Create lotgroup, checking for an existing one first."""
        created = not LotGroup.objects.filter(lot__in=lots).exists()
        lotgroup = lots[0].group_with(*lots[1:])
        if not lotgroup.added_reason:
            lotgroup.added_reason = lots[0].added_reason
            lotgroup.save()
        return lotgroup, created

    def get_use(self):
        return Use.objects.get_or_create(
            name='community garden',
            visible=True,
        )[0]

    def get_or_create_lot(self, bbl, parcel, row):
        try:
            return Lot.objects.get(bbl=bbl), False
        except Lot.DoesNotExist:
            print '\t\tNo lot found for %s. Creating.' % bbl
            kwargs = dict(self.lot_kwargs)
            kwargs.update({
                'address_line1': parcel.address,
                'bbl': bbl,
                'borough': borough_number[int(row['Boro'])],
                'block': get_int(row['Block']),
                'centroid': parcel.geom.centroid,
                'known_use': self.get_use(),
                'lot_number': get_int(row['Lot']),
                'owner': Owner.objects.get_or_create(name=parcel.ownername)[0],
                'polygon': parcel.geom,
                'postal_code': row['Zip'],
            })
            lot = Lot(**kwargs)
            lot.save()
            return lot, True

    def get_organizer(self, lot, row, **kwargs):
        url = row['HMTL'] # [sic]
        if not url or url == 'None' or not url.lower().startswith('http://'):
            url = None
        organizer = Organizer.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(Lot),
            object_id=lot.pk,
            name=kwargs['name'],
            type=OrganizerType.objects.get(name='community based organization'),
            defaults={
                'post_publicly': True,
                'url': url,
            },
        )[0]
        return organizer


    #
    # Shapefile-related functions
    #
    def open_gardens_shapefile(self, shp):
        return fiona.open(shp)

    def find_in_shapefile(self, shp, gardenid):
        """
        Attempt to find a garden with the given gardenid in the GrowNYC
        shapefile.
        """
        try:
            return filter(lambda f: f['properties']['GARDENID'] == int(gardenid), shp)[0]
        except IndexError:
            return None

    def create_lot_from_shp(self, feature, row):
        """
        Create a lot using a feature from the GrowNYC shapefile.
        """
        kwargs = dict(self.lot_kwargs)
        kwargs.update({
            'address_line1': row['descrip_ADDRESS'],
            'known_use': self.get_use(),
            'owner': Owner.objects.get_or_create(name=row['descrip_TYPE'])[0],
            'postal_code': row['Zip'],
        })
        return Lot.objects.create_lot_for_geom(
            GEOSGeometry(json.dumps(feature['geometry'])),
            **kwargs
        )
