# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creel_portal', '0004_auto_20170425_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strata',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strata', to='creel_portal.FN026'),
        ),
        migrations.AlterField(
            model_name='strata',
            name='daytype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strata', to='creel_portal.FN023'),
        ),
        migrations.AlterField(
            model_name='strata',
            name='mode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strata', to='creel_portal.FN028'),
        ),
        migrations.AlterField(
            model_name='strata',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strata', to='creel_portal.FN022'),
        ),
    ]
