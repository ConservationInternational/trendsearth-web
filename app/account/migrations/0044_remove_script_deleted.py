# Generated by Django 4.0a1 on 2022-01-29 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0043_script_run_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='script',
            name='deleted',
        ),
    ]
