# Generated by Django 4.0a1 on 2021-12-17 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('job', '0022_alter_job_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('layername', models.CharField(default='', max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('workspace', models.CharField(default='ldmp', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_result', models.BooleanField(default=False)),
                ('is_visible', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'db_table': 'layers',
            },
        ),
    ]
