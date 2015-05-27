# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NYCHADevelopment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('borough', models.CharField(max_length=13)),
                ('tds_num', models.CharField(max_length=3)),
                ('nonresidential_buildings', models.IntegerField()),
                ('residential_buildings', models.IntegerField()),
                ('units_in_2011', models.IntegerField()),
                ('population_in_2011', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
