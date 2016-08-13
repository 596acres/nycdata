"""
Community districts should be imported as a generic django-inplace boundary
in a layer called "community districts".

This app provides helpers for working with community districts but does not
store the boundary data.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CommunityDistrictDetails(models.Model):

    name = models.CharField(_('name'),
        max_length=256,
    )
    district = models.ForeignKey('boundaries.Boundary',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('district'),
    )
    borough = models.CharField(_('borough'),
        max_length=50,
    )
    chair = models.CharField(_('chair'),
        max_length=256,
        blank=True,
        null=True,
    )
    district_manager = models.CharField(_('district manager'),
        max_length=256,
        blank=True,
        null=True,
    )
    phone = models.CharField(_('phone'),
        max_length=50,
        blank=True,
        null=True,
    )
    email = models.EmailField(_('email'),
        blank=True,
        null=True,
    )
    url = models.URLField(_('url'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('community district details')
        verbose_name_plural = _('community district details')

    def __unicode__(self):
        return self.name
