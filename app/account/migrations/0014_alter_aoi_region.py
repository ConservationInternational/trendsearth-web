# Generated by Django 4.0a1 on 2021-11-18 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_aoi_buffer_size_aoi_city_aoi_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aoi',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.province'),
        ),
    ]
