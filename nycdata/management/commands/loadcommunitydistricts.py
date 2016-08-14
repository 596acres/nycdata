"""
Load community districts

"""
import csv
import re

from django.core.management.base import BaseCommand

from inplace.boundaries.models import Boundary

from ...boroughs import get_borough_number
from ...communitydistricts.models import CommunityDistrictDetails
from ...load import get_processed_data_file


class Command(BaseCommand):
    help = 'Loads community district details'

    filename = get_processed_data_file('communitydistrictsdetails/communitydistrictsdetails.csv')

    def handle(self, *args, **options):
        self.load_community_districts(csv.DictReader(open(self.filename, 'r')))

    def load_community_districts(self, rows):
        for row in rows:
            self.load_community_district(row)

    def load_community_district(self, row):
        try:
            district = Boundary.objects.get(
                label=self.make_district_label(row),
                layer__name='community districts',
            )
            community_district = CommunityDistrictDetails(
                district=district,
                borough=row['borough'],
                chair=row['chair'],
                district_manager=row['district_manager'],
                email=row['email'],
                name=row['name'],
                phone=row['phone'],
                url=row['website'],
            )
            community_district.save()
            print 'Added community district %s' % community_district
            return community_district
        except Boundary.DoesNotExist:
            print 'Could not find district %s. Skipping.' % row['name']
            return

    def make_district_label(self, row):
        return '%d%02d' % (
            get_borough_number(row['borough']),
            int(row['name'].replace('Community Board ', '')),
        )
