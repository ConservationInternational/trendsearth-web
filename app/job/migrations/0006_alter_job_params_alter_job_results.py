# Generated by Django 4.0a1 on 2021-11-27 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_alter_job_params_alter_job_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='params',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='job',
            name='results',
            field=models.JSONField(),
        ),
    ]
