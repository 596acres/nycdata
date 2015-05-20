from django.db import models


class UrbanRenewalRecord(models.Model):
    parcel = models.OneToOneField('parcels.Parcel')

    disposition_short = models.CharField(
        blank=True,
        max_length=75,
        null=True,
    )
    disposition_long = models.TextField(
        blank=True,
        null=True,
    )
    parking = models.BooleanField(default=False)
    plan_name = models.CharField(
        blank=True,
        max_length=75,
        null=True,
    )
