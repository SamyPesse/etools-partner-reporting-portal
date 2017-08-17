# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-07 21:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0006_auto_20170707_0552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partneractivity',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='partnerproject',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='partneractivity',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 7, 21, 47, 46, 800177, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partneractivity',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 7, 21, 47, 52, 200919, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partneractivity',
            name='status',
            field=models.CharField(choices=[('Ong', 'Ongoing'), ('Pla', 'Planned'), ('Com', 'Completed')], default='Ong', max_length=3),
        ),
    ]