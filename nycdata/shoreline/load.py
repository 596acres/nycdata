import os

from django.contrib.gis.utils import LayerMapping

from ..load import get_processed_data_file
from .models import Shoreline, shoreline_mapping


def load(**kwargs):
    from_shapefile(**kwargs)
    # TODO then write script to find parcels w/in 150ft of shoreline


def from_shapefile(strict=True, progress=True, verbose=False, **kwargs):
    """
    Load shoreline data into the database from the processed shapefile.
    """
    shp = get_processed_data_file(os.path.join('shoreline', 'shoreline-dissolved.shp'))
    mapping = LayerMapping(Shoreline, shp, shoreline_mapping, transform=False)
    mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)
