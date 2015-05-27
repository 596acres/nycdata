import os

from django.contrib.gis.utils import LayerMapping

from ..load import get_processed_data_file
from .models import NYCHADevelopment, nychadevelopment_mapping


def load(**kwargs):
    from_shapefile(**kwargs)


def from_shapefile(strict=True, progress=True, verbose=False, **kwargs):
    """
    Load NYCHA data into the database from the processed shapefile.
    """
    shp = get_processed_data_file(os.path.join('nycha', 'nycha.shp'))
    mapping = LayerMapping(NYCHADevelopment, shp, nychadevelopment_mapping,
                           transform=False)
    mapping.save(strict=strict, progress=progress, verbose=verbose, **kwargs)
