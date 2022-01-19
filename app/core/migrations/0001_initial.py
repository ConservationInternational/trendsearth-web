# Generated by Django 4.0a1 on 2021-11-16 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregationInputClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('name_short', models.CharField(max_length=50)),
                ('name_long', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'aggregation_input_class',
            },
        ),
        migrations.CreateModel(
            name='AggregationOutputClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('name_short', models.CharField(max_length=50)),
                ('name_long', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'aggregation_output_class',
            },
        ),
        migrations.CreateModel(
            name='UserAggregationClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.aggregationinputclass')),
                ('outputclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.aggregationoutputclass')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'db_table': 'user_aggregation_class',
            },
        ),
    ]