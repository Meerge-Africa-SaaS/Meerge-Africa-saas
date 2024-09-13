# Generated by Django 5.0.8 on 2024-09-13 22:51

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='email_code',
            field=models.CharField(default=core.models.get_default_email_code, max_length=6),
        ),
    ]
