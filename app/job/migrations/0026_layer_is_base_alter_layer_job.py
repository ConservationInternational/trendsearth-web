# Generated by Django 4.0a1 on 2021-12-20 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0025_alter_layer_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='is_base',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='layer',
            name='job',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.job'),
        ),
    ]
