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
            name='CityCouncilMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='email', blank=True)),
                ('url', models.URLField(null=True, verbose_name='url', blank=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='district', to='boundaries.Boundary', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
