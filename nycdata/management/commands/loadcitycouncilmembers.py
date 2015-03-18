"""
Load city council members.

"""
import csv
import re

from django.core.management.base import BaseCommand

from inplace.boundaries.models import Boundary

from ...citycouncildistricts.models import CityCouncilMember


class Command(BaseCommand):
    args = 'filename'
    help = 'Loads city council members'

    number_pattern = re.compile('.*?(\d+).*')
    url_pattern = 'http://council.nyc.gov/d%s/html/members/home.shtml'

    def handle(self, filename, *args, **options):
        self.load_city_council_members(csv.DictReader(open(filename, 'r')))

    def load_city_council_members(self, rows):
        for row in rows:
            self.load_city_council_member(row)

    def load_city_council_member(self, row):
        district_number = self.parse_district_number(row['district'])
        try:
            district = Boundary.objects.get(
                label=district_number,
                layer__name='city council districts',
            )
            member = CityCouncilMember(
                district=district,
                name=row['name'],
                url=self.make_url(district.label),
            )
            member.save()
            print 'Added city council member %s' % member
            return member
        except Boundary.DoesNotExist:
            print 'Could not find district %s. Skipping.' % district_number
            return

    def make_url(self, district_number):
        return self.url_pattern % district_number

    def parse_district_number(self, district_field):
        # Find number, convert to int (remove leading 0s), convert back to str
        return str(int(self.number_pattern.match(district_field).group(1)))
