# Generated by Django 4.0a1 on 2022-01-29 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0027_delete_scriptstatus'),
        ('account', '0040_delete_algorithmrunmode_remove_algorithm_item_type_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExecutionScript',
            new_name='Script',
        ),
        migrations.AlterModelTable(
            name='script',
            table='script',
        ),
    ]