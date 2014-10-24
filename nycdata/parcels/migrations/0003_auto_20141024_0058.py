# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0002_auto_20141010_1132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parcel',
            old_name='lot',
            new_name='lot_number',
        ),
    ]
