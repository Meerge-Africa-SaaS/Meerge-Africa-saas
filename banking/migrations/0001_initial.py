# Generated by Django 5.0.6 on 2024-11-12 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=128)),
                ('account_holder_name', models.CharField(max_length=128)),
                ('iban', models.CharField(blank=True, max_length=34, null=True)),
                ('swift_code', models.CharField(blank=True, max_length=11, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Account Detail',
                'verbose_name_plural': 'Account Details',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
    ]
