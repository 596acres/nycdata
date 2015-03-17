"""
City council districts should be imported as a generic django-inplace boundary
in a layer called "city council districts".

This app provides helpers for working with city council districts but does not
store the boundary data.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CityCouncilMember(models.Model):

    name = models.CharField(_('name'),
        max_length=256,
    )
    district = models.ForeignKey('boundaries.Boundary',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('district'),
    )
    email = models.EmailField(_('email'),
        blank=True,
        null=True,
    )
    url = models.URLField(_('url'),
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.name
