# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0005_tripset_trips'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripset',
            name='trips',
            field=models.ManyToManyField(blank=True, to='taxi.Trip'),
        ),
    ]
