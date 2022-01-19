# Generated by Django 4.0a1 on 2021-12-02 22:11

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_alter_city_name_de_alter_city_name_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='code',
            field=models.CharField(blank=True, default=django.db.models.fields.UUIDField, max_length=5, null=True),
        ),
    ]