# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-25 05:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170824_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatewaytype',
            name='admin_level',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]