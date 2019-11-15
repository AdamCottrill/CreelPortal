# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creel_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='strata',
            options={'ordering': ['creel_run__creel__prj_cd', 'creel_run__run', 'stratum_label']},
        ),
        migrations.RenameField(
            model_name='strata',
            old_name='stratum',
            new_name='stratum_label',
        ),
        migrations.RemoveField(
            model_name='strata',
            name='creel',
        ),
        migrations.AddField(
            model_name='strata',
            name='creel_run',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='strata', to='creel_portal.FR711'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fr711',
            name='mask_c',
            field=models.CharField(default='++_++_++_++', max_length=11),
        ),
        migrations.AlterField(
            model_name='fr711',
            name='run',
            field=models.CharField(default='01', max_length=2),
        ),
    ]
