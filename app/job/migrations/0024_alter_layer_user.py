# Generated by Django 4.0a1 on 2021-12-17 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('job', '0023_layer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
