# Generated by Django 4.0a1 on 2021-11-17 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_city_country_province_country_alter_nation_crs'),
    ]

    operations = [
        migrations.AddField(
            model_name='aoi',
            name='buffer_size',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='aoi',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.city'),
        ),
        migrations.AddField(
            model_name='aoi',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.nation'),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.region'),
        ),
    ]
