from inplace.boundaries.models import Boundary


def find_borough(point):
    """Find the borough that contains the given point."""
    try:
        return Boundary.objects.get(
            layer__name='boroughs',
            geometry__contains=point,
        )
    except Boundary.DoesNotExist:
        return None
