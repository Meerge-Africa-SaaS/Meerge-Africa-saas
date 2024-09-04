# Generated by Django 5.0.6 on 2024-08-24 09:27

import django.core.validators
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_emailverification_email_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='email_code',
            field=models.CharField(default='2a9edd', max_length=6),
        ),
        migrations.AlterField(
            model_name='smsverification',
            name='sms_code',
            field=models.CharField(default='fa67a3', max_length=6),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(error_messages={'unique': 'A user with that phone number already exists.'}, max_length=128, region=None, unique=True, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, db_index=True, error_messages={'unique': 'A user with that username already exists.'}, max_length=50, null=True, validators=[django.core.validators.RegexValidator(code='Invalid Username.', message="Username must be Alpha-Numeric and may also contain '.', '@' and '_'.", regex='^[a-zA-Z0-9.@_]*$')], verbose_name='username'),
        ),
    ]
