# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('borough', models.CharField(max_length=2)),
                ('block', models.IntegerField()),
                ('lot', models.IntegerField()),
                ('cd', models.IntegerField()),
                ('ct2010', models.CharField(max_length=7)),
                ('cb2010', models.CharField(max_length=5)),
                ('schooldist', models.CharField(max_length=2)),
                ('council', models.IntegerField()),
                ('zipcode', models.IntegerField()),
                ('firecomp', models.CharField(max_length=4)),
                ('policeprct', models.IntegerField()),
                ('address', models.CharField(max_length=28)),
                ('zonedist1', models.CharField(max_length=9)),
                ('zonedist2', models.CharField(max_length=9)),
                ('zonedist3', models.CharField(max_length=9)),
                ('zonedist4', models.CharField(max_length=9)),
                ('overlay1', models.CharField(max_length=4)),
                ('overlay2', models.CharField(max_length=4)),
                ('spdist1', models.CharField(max_length=6)),
                ('spdist2', models.CharField(max_length=6)),
                ('ltdheight', models.CharField(max_length=5)),
                ('allzoning1', models.CharField(max_length=27)),
                ('allzoning2', models.CharField(max_length=21)),
                ('splitzone', models.CharField(max_length=1)),
                ('bldgclass', models.CharField(max_length=2)),
                ('landuse', models.CharField(max_length=2)),
                ('easements', models.IntegerField()),
                ('ownertype', models.CharField(max_length=1)),
                ('ownername', models.CharField(max_length=21)),
                ('lotarea', models.IntegerField()),
                ('bldgarea', models.IntegerField()),
                ('comarea', models.IntegerField()),
                ('resarea', models.IntegerField()),
                ('officearea', models.IntegerField()),
                ('retailarea', models.IntegerField()),
                ('garagearea', models.IntegerField()),
                ('strgearea', models.IntegerField()),
                ('factryarea', models.IntegerField()),
                ('otherarea', models.IntegerField()),
                ('areasource', models.CharField(max_length=1)),
                ('numbldgs', models.IntegerField()),
                ('numfloors', models.FloatField()),
                ('unitsres', models.IntegerField()),
                ('unitstotal', models.IntegerField()),
                ('lotfront', models.FloatField()),
                ('lotdepth', models.FloatField()),
                ('bldgfront', models.FloatField()),
                ('bldgdepth', models.FloatField()),
                ('ext', models.CharField(max_length=2)),
                ('proxcode', models.CharField(max_length=1)),
                ('irrlotcode', models.CharField(max_length=1)),
                ('lottype', models.CharField(max_length=1)),
                ('bsmtcode', models.CharField(max_length=1)),
                ('assessland', models.FloatField()),
                ('assesstot', models.FloatField()),
                ('exemptland', models.FloatField()),
                ('exempttot', models.FloatField()),
                ('yearbuilt', models.IntegerField()),
                ('builtcode', models.CharField(max_length=1)),
                ('yearalter1', models.IntegerField()),
                ('yearalter2', models.IntegerField()),
                ('histdist', models.CharField(max_length=40)),
                ('landmark', models.CharField(max_length=35)),
                ('builtfar', models.FloatField()),
                ('residfar', models.FloatField()),
                ('commfar', models.FloatField()),
                ('facilfar', models.FloatField()),
                ('borocode', models.IntegerField()),
                ('bbl', models.DecimalField(max_digits=10, decimal_places=0)),
                ('condono', models.IntegerField()),
                ('tract2010', models.CharField(max_length=6)),
                ('xcoord', models.IntegerField()),
                ('ycoord', models.IntegerField()),
                ('zonemap', models.CharField(max_length=3)),
                ('zmcode', models.CharField(max_length=1)),
                ('sanborn', models.CharField(max_length=8)),
                ('taxmap', models.CharField(max_length=5)),
                ('edesignum', models.CharField(max_length=5)),
                ('appbbl', models.FloatField()),
                ('appdate', models.CharField(max_length=10)),
                ('plutomapid', models.CharField(max_length=1)),
                ('version', models.CharField(max_length=4)),
                ('mappluto_f', models.IntegerField()),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
