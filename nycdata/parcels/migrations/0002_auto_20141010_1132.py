# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='bbl',
            field=models.DecimalField(max_digits=10, decimal_places=0, db_index=True),
        ),
    ]
