# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-16 23:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20171217_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='timezone',
        ),
    ]
