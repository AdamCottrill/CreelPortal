# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creel_portal', '0005_auto_20170425_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='strata',
            name='period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strata', to='creel_portal.FN024'),
        ),
    ]
