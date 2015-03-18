"""
Load community districts

"""
import csv
import re

from django.core.management.base import BaseCommand

from inplace.boundaries.models import Boundary

from ...boroughs import get_borough_number
from ...communitydistricts.models import CommunityDistrictDetails


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads community district details'

    def handle(self, filename, *args, **options):
        self.load_community_districts(csv.DictReader(open(filename, 'r')))

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
