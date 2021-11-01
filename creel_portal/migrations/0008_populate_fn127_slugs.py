# Generated by Django 2.2.7 on 2021-11-01 21:12

from django.db import migrations


def populate_fn127_slugs(apps, schema_editor):
    """to populate the slug for each age estimates, just call the save method."""
    FN127 = apps.get_model("creel_portal", "FN127")
    for item in FN127.objects.all():
        item.save()


def clear_fn127_slugs(apps, schema_editor):
    """"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("creel_portal", "0007_missing_fn127_fields"),
    ]

    operations = [
        migrations.RunPython(populate_fn127_slugs, reverse_code=clear_fn127_slugs)
    ]