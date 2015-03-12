import re

from ..boroughs import get_borough_number


int_regex = re.compile(r'\D*(\d+)\D*')


def _get_int(value):
    try:
        return int(value)
    except ValueError:
        # Try to just get digits
        return int(re.match(int_regex, value).group(1))


def build_bbl(borough, block, lot):
    """
    Build a BBL given the constituent borough, block and lot.

    BBLs are unique identifiers for tax lots in New York City.
    """
    # Accept borough as string but convert it first
    try:
        borough = int(borough)
    except ValueError:
        borough = get_borough_number(borough)

    return '%d%05d%04d' % (borough, _get_int(block), _get_int(lot))
