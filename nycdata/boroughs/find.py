from inplace.boundaries.models import Boundary


def find_borough(point, polygon=None):
    """Find the borough that contains the given point."""
    try:
        return Boundary.objects.get(
            layer__name='boroughs',
            geometry__contains=point,
        )
    except Boundary.DoesNotExist:
        if polygon:
            try:
                return Boundary.objects.get(
                    layer__name='boroughs',
                    geometry__overlaps=polygon
                )
            except Boundary.DoesNotExist:
                pass
    return None
