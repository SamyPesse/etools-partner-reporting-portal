# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 07:45
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('partner', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryProgrammeOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LowerLevelOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255)),
                ('cp_output', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ll_outputs', to='unicef.CountryProgrammeOutput')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('phone_number', models.CharField(max_length=64, verbose_name='Phone Number')),
                ('email', models.CharField(max_length=255, verbose_name='Phone Number')),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammeDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('agreement', models.CharField(max_length=255, verbose_name='Agreement')),
                ('document_type', models.CharField(choices=[('PD', 'Programme Document'), ('SHP', 'Simplified Humanitarian Programme Document'), ('SSF', 'SSFA TOR')], default='PD', max_length=3, verbose_name='Document Type')),
                ('reference_number', models.CharField(max_length=255, verbose_name='Reference Number')),
                ('title', models.CharField(max_length=255, verbose_name='PD/SSFA ToR Title')),
                ('unicef_office', models.CharField(max_length=255, verbose_name='UNICEF Office(s)')),
                ('start_date', models.DateField(verbose_name='Start Programme Date')),
                ('end_date', models.DateField(verbose_name='Due Date')),
                ('population_focus', models.CharField(max_length=256, verbose_name='Population Focus')),
                ('status', models.CharField(choices=[('Dra', 'Draft'), ('Act', 'Active'), ('Imp', 'Implemented'), ('Rej', 'Rejected')], default='Dra', max_length=256, verbose_name='PD/SSFA status')),
                ('contributing_to_cluster', models.BooleanField(default=True, verbose_name='Contributing to Cluster')),
                ('frequency', models.CharField(choices=[('Wee', 'Weekly'), ('Mon', 'Monthly'), ('Qua', 'Quarterly'), ('Csd', 'Custom specific dates')], default='Mon', max_length=3, verbose_name='Frequency of reporting')),
                ('budget', models.DecimalField(blank=True, decimal_places=2, help_text='Total Budget', max_digits=12, null=True)),
                ('budget_currency', models.CharField(choices=[('USD', '$'), ('EUR', 'E')], default='USD', max_length=16, verbose_name='Budget Currency')),
                ('cso_contribution', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='CSO Contribution')),
                ('cso_contribution_currency', models.CharField(choices=[('USD', '$'), ('EUR', 'E')], default='USD', max_length=16, verbose_name='CSO Contribution Currency')),
                ('total_unicef_cash', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='UNICEF cash')),
                ('total_unicef_cash_currency', models.CharField(choices=[('USD', '$'), ('EUR', 'E')], default='USD', max_length=16, verbose_name='UNICEF cash Currency')),
                ('in_kind_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='UNICEF Supplies')),
                ('in_kind_amount_currency', models.CharField(choices=[('USD', '$'), ('EUR', 'E')], default='USD', max_length=16, verbose_name='UNICEF Supplies Currency')),
                ('cs_dates', django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), default=list, size=None)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.Partner')),
                ('partner_focal_point', models.ManyToManyField(related_name='partner_focal_programme_documents', to='unicef.Person', verbose_name='Partner Focal Point(s)')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProgressReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('partner_contribution_to_date', models.CharField(max_length=256)),
                ('funds_received_to_date', models.CharField(max_length=256)),
                ('challenges_in_the_reporting_period', models.CharField(max_length=256)),
                ('proposed_way_forward', models.CharField(max_length=256)),
                ('status', models.CharField(choices=[('Due', 'Due'), ('Ove', 'Overdue'), ('Sub', 'Submitted'), ('Sen', 'Sent back'), ('Acc', 'Accepted')], default='Due', max_length=3)),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('submission_date', models.DateField(blank=True, null=True, verbose_name='Submission Date')),
                ('sent_back_date', models.DateField(blank=True, null=True, verbose_name='Sent Back Date')),
                ('sent_back_feedback', models.TextField(blank=True, null=True)),
                ('programme_document', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='progress_reports', to='unicef.ProgrammeDocument')),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='programmedocument',
            name='sections',
            field=models.ManyToManyField(to='unicef.Section'),
        ),
        migrations.AddField(
            model_name='programmedocument',
            name='unicef_focal_point',
            field=models.ManyToManyField(related_name='unicef_focal_programme_documents', to='unicef.Person', verbose_name='UNICEF Focal Point(s)'),
        ),
        migrations.AddField(
            model_name='programmedocument',
            name='unicef_officers',
            field=models.ManyToManyField(related_name='officer_programme_documents', to='unicef.Person', verbose_name='UNICEF Officer(s)'),
        ),
        migrations.AddField(
            model_name='programmedocument',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_focal_programme_documents', to='core.Workspace'),
        ),
        migrations.AddField(
            model_name='countryprogrammeoutput',
            name='programme_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cp_outputs', to='unicef.ProgrammeDocument'),
        ),
    ]
