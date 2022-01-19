# Generated by Django 4.0a1 on 2021-11-17 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_rename_name_city_region_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.nation'),
        ),
        migrations.AddField(
            model_name='province',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.nation'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='crs',
            field=models.IntegerField(default=4326),
        ),
    ]