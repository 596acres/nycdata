# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-10 16:56
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postoffices', '0002_auto_20160809_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postoffice',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]