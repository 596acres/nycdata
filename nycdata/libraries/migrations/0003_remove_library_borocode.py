# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 19:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0002_auto_20160730_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='borocode',
        ),
    ]
