# Generated by Django 3.2.8 on 2021-10-19 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20211020_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.algorithm'),
        ),
    ]
