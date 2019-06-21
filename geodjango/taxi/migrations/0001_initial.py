# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 15:36
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorID', models.SmallIntegerField(blank=True, null=True)),
                ('pickupTime', models.DateTimeField(blank=True, null=True)),
                ('dropoffTime', models.DateTimeField(blank=True, null=True)),
                ('storeAndFwdFlag', models.BooleanField()),
                ('rateCodeID', models.SmallIntegerField(blank=True, null=True)),
                ('pickupPoint', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('dropoffPoint', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('passengerCount', models.SmallIntegerField(blank=True, null=True)),
                ('tripDistance', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('fareAmount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('extra', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('MTATax', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('tipAmount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('tolls_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('improvementSurcharge', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('totalAmount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('paymentType', models.SmallIntegerField(blank=True, null=True)),
                ('tripType', models.SmallIntegerField(blank=True, null=True)),
                ('PULocationID', models.SmallIntegerField(blank=True, null=True)),
                ('DOLocationID', models.SmallIntegerField(blank=True, null=True)),
            ],
        ),
    ]