# Generated by Django 4.0a1 on 2021-12-10 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0018_alter_job_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='results',
            field=models.JSONField(verbose_name={}),
        ),
    ]