from django import template

from ...boroughs import borough_number

register = template.Library()


def community_district_label(value):
    return '%s %d' % (
        borough_number[int(value[0])],
        int(value[1:]),
    )


register.filter('community_district_label', community_district_label)
