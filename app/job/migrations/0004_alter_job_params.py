# Generated by Django 4.0a1 on 2021-11-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_remove_job_joblocalresult_remove_job_jobcloudresult_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='params',
            field=models.JSONField(default={}),
        ),
    ]
