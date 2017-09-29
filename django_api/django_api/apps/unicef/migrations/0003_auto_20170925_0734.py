# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('unicef', '0002_auto_20170924_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='countryprogrammeoutput',
            name='external_id',
            field=models.CharField(blank=True, help_text='An ID representing this instance in an external system', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='lowerleveloutput',
            name='external_id',
            field=models.CharField(blank=True, help_text='An ID representing this instance in an external system', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='person',
            name='external_id',
            field=models.CharField(blank=True, help_text='An ID representing this instance in an external system', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='programmedocument',
            name='external_id',
            field=models.CharField(blank=True, help_text='An ID representing this instance in an external system', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='section',
            name='external_id',
            field=models.CharField(blank=True, help_text='An ID representing this instance in an external system', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]