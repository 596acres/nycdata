# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boundaries', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityDistrictDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('borough', models.CharField(max_length=50, verbose_name='borough')),
                ('chair', models.CharField(max_length=256, null=True, verbose_name='chair', blank=True)),
                ('district_manager', models.CharField(max_length=256, null=True, verbose_name='district manager', blank=True)),
                ('phone', models.CharField(max_length=50, null=True, verbose_name='phone', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='email', blank=True)),
                ('url', models.URLField(null=True, verbose_name='url', blank=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='district', to='boundaries.Boundary', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
