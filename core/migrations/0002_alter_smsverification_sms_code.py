# Generated by Django 5.0.6 on 2024-08-31 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsverification',
            name='sms_code',
            field=models.CharField(default='01d203', max_length=6),
        ),
    ]