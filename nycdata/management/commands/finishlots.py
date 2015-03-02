#
# Finish loading lots exported from original database
#
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from livinglots_usercontent.files.models import File
from livinglots_usercontent.notes.models import Note
from livinglots_usercontent.photos.models import Photo
from lots.models import Lot
from nycdata.parcels.models import Parcel
from steward.models import StewardProject


class Command(BaseCommand):
    help = 'Finish loading NYC lots exported from original database'

    def finish_lots(self):
        for lot in Lot.objects.all():
            # Get lot to set acres
            lot.area_acres

            # Get lot to set layers
            lot.save()

    def create_new_lot(self, parcel, lots):
        print "Creating new lot for %s" % str(parcel.bbl)
        borough, owner, known_use_certainty, known_use_locked, known_use = (
            None, None, None, None, None
        )

        boroughs = list(set([l.borough for l in lots]))
        if len(boroughs) == 1:
            borough = boroughs[0]
        else:
            print "\t * Couldn't pick a borough", boroughs, lots
            raise Exception("Not able to pick borough, something's weird!")

        owners = list(set([l.owner for l in lots]))
        if len(owners) == 1:
            owner = owners[0]
        else:
            print "\t * Couldn't pick an owner", owners

        known_use_certainties = list(set([l.known_use_certainty for l in lots]))
        if len(known_use_certainties) == 1:
            known_use_certainty = known_use_certainties[0]
        else:
            print "\t * Couldn't pick a known_use_certainty", known_use_certainties

        known_use_lockeds = list(set([l.known_use_locked for l in lots]))
        if len(known_use_lockeds) == 1:
            known_use_locked = known_use_lockeds[0]
        else:
            print "\t * Couldn't pick a known_use_locked", known_use_lockeds

        known_uses = list(set([l.known_use for l in lots]))
        if len(known_uses) == 1:
            known_use = known_uses[0]
        else:
            print "\t * Couldn't pick a known_use", known_uses
            known_use_certainty = 0
            known_use_locked = False

        newlot = Lot(
            centroid=parcel.geom.centroid,
            polygon=parcel.geom,
            address_line1=parcel.address,
            postal_code=parcel.zipcode,
            state_province='NY',
            country='USA',
            added_reason='Created for duplicate lots during import',
            bbl=None, # Another lot might be using this bbl, handle it later
            block=parcel.block,
            lot_number=parcel.lot_number,

            borough=borough,
            owner=owner,
            known_use=known_use,
            known_use_certainty=known_use_certainty,
            known_use_locked=known_use_locked,
        )
        newlot.save()
        return newlot

    def move_duplicate_relateds(self, newlot, oldlot):
        # Move organizers
        for organizer in oldlot.organizers.all():
            organizer.content_object = newlot
            organizer.save()

        ct = ContentType.objects.get_for_model(oldlot)

        generic_kwargs = {
            'content_type': ct,
            'object_id': oldlot.pk,
        }

        # Move files
        for f in File.objects.filter(**generic_kwargs):
            f.content_object = newlot
            f.save()

        # Move photos
        for p in Photo.objects.filter(**generic_kwargs):
            p.content_object = newlot
            p.save()

        # Move notes
        for n in Note.objects.filter(**generic_kwargs):
            n.content_object = newlot
            n.save()

        # Move steward projects
        for sp in StewardProject.objects.filter(**generic_kwargs):
            sp.content_object = newlot
            sp.save()

    def fix_lots_on_same_parcel(self):
        """
        Find all lots sharing the same parcel and fix them. This is likely
        because the lots have changed / merged since the original 596 data was
        created.
        """
        dupes = Lot.objects.values('parcel__bbl').annotate(c=Count('pk')).filter(
            c__gt=1,
            parcel__bbl__isnull=False
        )

        for parcel_bbl in [d['parcel__bbl'] for d in dupes]:
            parcel = Parcel.objects.get(bbl=parcel_bbl)
            lots = Lot.objects.filter(parcel__bbl=parcel_bbl)

            try:
                newlot = self.create_new_lot(parcel, lots)
            except Exception:
                continue

            print 'Consolidating', [l.bbl for l in lots], 'into', parcel

            for lot in lots:
                self.move_duplicate_relateds(newlot, lot)
                lot.delete()

            newlot.bbl = parcel_bbl
            newlot.save()

    def handle(self, *args, **options):
        self.fix_lots_on_same_parcel()
        self.finish_lots()
