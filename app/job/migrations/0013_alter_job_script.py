# Generated by Django 4.0a1 on 2021-12-01 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_alter_city_name_de_alter_city_name_en_and_more'),
        ('job', '0012_job_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='script',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.executionscript'),
        ),
    ]
