# Generated by Django 4.0a1 on 2021-11-05 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_aoi_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.country'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organization',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.region'),
        ),
    ]
