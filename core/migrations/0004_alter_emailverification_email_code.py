# Generated by Django 5.1.3 on 2024-11-10 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_emailverification_email_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='email_code',
            field=models.CharField(default='004915', max_length=6),
        ),
    ]
