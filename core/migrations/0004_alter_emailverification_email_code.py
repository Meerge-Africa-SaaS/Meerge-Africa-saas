

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_emailverification_email_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='email_code',

        ),
    ]
