# Generated by Django 4.0a1 on 2021-11-28 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_job_params'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='results',
        ),
    ]