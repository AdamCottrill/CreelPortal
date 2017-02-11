# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 03:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creel_portal', '0003_auto_20170210_2332'),
    ]

    operations = [
        migrations.CreateModel(
            name='FN125',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grp', models.CharField(max_length=2)),
                ('fish', models.IntegerField()),
                ('flen', models.IntegerField(blank=True, null=True)),
                ('tlen', models.IntegerField(blank=True, null=True)),
                ('rwt', models.IntegerField(blank=True, null=True)),
                ('sex', models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (9, 'Unknown')], default=None, null=True)),
                ('gon', models.CharField(blank=True, max_length=2, null=True)),
                ('mat', models.IntegerField(blank=True, choices=[(1, 'Immature'), (2, 'Mature'), (9, 'Unknown')], default=None, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('agest', models.CharField(blank=True, max_length=8, null=True)),
                ('clipc', models.CharField(blank=True, max_length=6, null=True)),
                ('fate', models.CharField(blank=True, max_length=2, null=True)),
                ('catch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creel_portal.FN123')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creel_portal.Species')),
            ],
            options={
                'verbose_name': 'Fish',
                'ordering': ['catch', 'species', 'fish'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='fn125',
            unique_together=set([('catch', 'species', 'grp', 'fish')]),
        ),
    ]