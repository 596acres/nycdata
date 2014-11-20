from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

register = template.Library()


class SortCityCouncilDistricts(AsTag):
    options = Options(
        Argument('city_council_districts', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, city_council_districts):
        return sorted(city_council_districts, key=lambda d: int(d.label))


register.tag(SortCityCouncilDistricts)
