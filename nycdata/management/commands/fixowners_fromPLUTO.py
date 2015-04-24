#
# Somehow the owners of lots have been deleted. This will restore them without
# a file from 596acres.org, using PLUTO data.
#
import csv

from django.core.management.base import BaseCommand

from lots.models import Lot
from owners.models import Owner

from nycdata.imports.utils import get_lot


class Command(BaseCommand):
    args = 'outfilename'
    help = "Fix lots' owners using PLUTO data"

    def handle(self, outfilename, *args, **options):
        with open(outfilename, 'a') as outfile:
            self.outfile_writer = csv.DictWriter(outfile, fieldnames=[
                'bbl',
                'pk',
                'llnyc_org_owner',
                'PLUTO_owner',
                'action',
            ])
            self.fix_owners()

    def fix_owners(self):
        for lot in Lot.objects.filter(owner__isnull=True):
            current_owner = lot.owner
            try:
                old_owner = self.get_owner(name=lot.parcel.ownername)
            except Exception:
                old_owner = None

            if not (current_owner or old_owner):
                print "(%s|%d) Didn't find an owner for the lot. Skipping." % (lot.bbl, lot.pk)
                self.record_action(lot, current_owner, old_owner, 'no owners, skipped')
                continue
            if current_owner == old_owner:
                print '(%s|%d) Owners match. Skipping.' % (lot.bbl, lot.pk)
                self.record_action(lot, current_owner, old_owner, 'owners matched, skipped')
                continue

            answer = raw_input('(%s|%d) Current: %s, old: %s. Use old? (Y/n/a) ' % (
                lot.bbl,
                lot.pk,
                current_owner,
                old_owner,
            ))
            if answer.lower() == 'a':
                current_owner.make_alias(old_owner)
                continue
            if answer == '' or answer.lower() == 'y':
                lot.owner = old_owner
                lot.save()

                # Save parent lot group just in case
                if lot.group:
                    lot.group.save()
                self.record_action(lot, current_owner, old_owner, 'use PLUTO')
            else:
                self.record_action(lot, current_owner, old_owner, 'keep llnyc')

    def get_owner(self, name=None, type=None, **kwargs):
        return Owner.objects.get_or_create(name=name)[0]

    def record_action(self, lot, current_owner, old_owner, action):
        row = {
            'action': action,
            'bbl': lot.bbl,
            'pk': lot.pk,
        }
        if current_owner:
            row['llnyc_org_owner'] = current_owner.name
        if old_owner:
            row['PLUTO_owner'] = old_owner.name
        self.outfile_writer.writerow(row)
