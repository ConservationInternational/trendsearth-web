# Generated by Django 4.0a1 on 2021-11-30 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_remove_profile_country_remove_profile_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='country',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]
