# Generated by Django 4.0a1 on 2022-01-29 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0026_layer_is_base_alter_layer_job'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ScriptStatus',
        ),
    ]