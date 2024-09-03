from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsverification',
            name='sms_code',
            field=models.CharField(default='72578b', max_length=6),
        ),
    ]
