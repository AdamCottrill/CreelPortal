# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 14:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creel_portal', '0003_auto_20170425_1026'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='strata',
            unique_together=set([('creel_run', 'stratum_label')]),
        ),
    ]
