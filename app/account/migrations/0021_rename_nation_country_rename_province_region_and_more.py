# Generated by Django 4.0a1 on 2021-11-30 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_remove_region_country_delete_country_delete_region'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Nation',
            new_name='Country',
        ),
        migrations.RenameModel(
            old_name='Province',
            new_name='Region',
        ),
        migrations.AlterModelTable(
            name='country',
            table='country',
        ),
        migrations.AlterModelTable(
            name='region',
            table='region',
        ),
    ]
