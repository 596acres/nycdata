from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

register = template.Library()


class GetCommunityDistrictDetails(AsTag):
    options = Options(
        Argument('district', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, district):
        try:
            return district.communitydistrictdetails_set.all()[0]
        except IndexError:
            return None


register.tag(GetCommunityDistrictDetails)
