# Generated by Django 5.0.6 on 2024-08-14 03:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='restaurants',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
        migrations.DeleteModel(
            name='Chef',
        ),
    ]
