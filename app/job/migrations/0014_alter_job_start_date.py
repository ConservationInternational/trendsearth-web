# Generated by Django 4.0a1 on 2021-12-06 18:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0013_alter_job_script'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='start_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
