from lots.models import Lot, LotGroup


def get_lot(bbl):
    try:
        return LotGroup.objects.get(lot__bbl=bbl)
    except LotGroup.DoesNotExist:
        return Lot.objects.get(bbl=bbl)
