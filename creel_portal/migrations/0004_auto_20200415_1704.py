# Generated by Django 2.2.7 on 2020-04-15 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creel_portal', '0003_auto_20200409_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fn111',
            name='comment1',
            field=models.TextField(blank=True, help_text='Comments about current interview period.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='fr715',
            name='ang_fn',
            field=models.CharField(choices=[('agnvis', 'ANGVIS'), ('angorig', 'ANGORIG'), ('angmeth', 'ANGMETH'), ('angguid', 'ANGGUID'), ('angop1', 'ANGOP1'), ('angop2', 'ANGOP2'), ('angop3', 'ANGOP3'), ('angop4', 'ANGOP4'), ('angop5', 'ANGOP5')], max_length=8),
        ),
    ]
