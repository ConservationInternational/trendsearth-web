# Generated by Django 4.0a1 on 2021-11-27 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_alter_job_params_alter_job_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='params',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='job',
            name='results',
            field=models.TextField(),
        ),
    ]
