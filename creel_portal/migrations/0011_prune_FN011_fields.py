# Generated by Django 2.2.18 on 2022-01-27 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creel_portal', '0010_missing_fn126_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fn011',
            name='aru',
        ),
        migrations.RemoveField(
            model_name='fn011',
            name='fof_loc',
        ),
        migrations.RemoveField(
            model_name='fn011',
            name='fof_nm',
        ),
        migrations.RemoveField(
            model_name='fn011',
            name='prj_his',
        ),
        migrations.RemoveField(
            model_name='fn011',
            name='prj_size',
        ),
        migrations.RemoveField(
            model_name='fn011',
            name='prj_ver',
        ),
        migrations.RemoveField(
            model_name='fn011',
            name='v0',
        ),
        migrations.RemoveField(
            model_name='fn011',
            name='wby',
        ),
        migrations.RemoveField(
            model_name='fn011',
            name='wby_nm',
        ),
        migrations.AlterField(
            model_name='fn125',
            name='sex',
            field=models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Hermaphrodite'), (9, 'Unknown')], default=None, null=True),
        ),
    ]