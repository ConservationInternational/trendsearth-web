# Generated by Django 4.0a1 on 2021-12-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0015_remove_cloudresults_bands_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='results',
            field=models.JSONField(default={}),
        ),
    ]
