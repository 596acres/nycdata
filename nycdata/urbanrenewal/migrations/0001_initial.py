# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0003_auto_20141024_0058'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrbanRenewalRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disposition_short', models.CharField(max_length=75, null=True, blank=True)),
                ('disposition_long', models.TextField(null=True, blank=True)),
                ('parking', models.BooleanField(default=False)),
                ('plan_name', models.CharField(max_length=75, null=True, blank=True)),
                ('parcel', models.OneToOneField(to='parcels.Parcel')),
            ],
        ),
    ]
