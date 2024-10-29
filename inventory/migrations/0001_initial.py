# Generated by Django 5.1.1 on 2024-10-26 11:16

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banking', '__first__'),
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Item Categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('unit_of_measure', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.itemcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('quantity', models.IntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('SKU_number', models.CharField(blank=True, max_length=60, null=True)),
                ('product_name', models.CharField(blank=True, max_length=60, null=True)),
                ('product_image', models.URLField(blank=True, null=True)),
                ('product_category', models.CharField(blank=True, max_length=60, null=True)),
                ('manufacture_name', models.CharField(blank=True, max_length=60, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit_available', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('size', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('discount_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('pickup_available', models.BooleanField(blank=True, default=False, null=True, verbose_name='Pickup Available')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.item')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('business_section_name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('store_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=256, unique=True, verbose_name='email address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, error_messages={'unique': 'A restaurant with that phone number already exists.'}, max_length=128, null=True, region=None, unique=True, verbose_name='phone number')),
                ('cac_reg_number', models.CharField(blank=True, max_length=20, null=True)),
                ('cac_certificate', models.URLField(blank=True, null=True)),
                ('business_license', models.URLField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('profile_img', models.URLField(blank=True, null=True)),
                ('cover_img', models.URLField(blank=True, null=True)),
                ('address', models.CharField(max_length=130)),
                ('category', models.ManyToManyField(related_name='suppliers', to='inventory.category')),
                ('city', models.ManyToManyField(related_name='suppliers', to='cities_light.city')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.supplier'),
        ),
        migrations.CreateModel(
            name='SupplyManager',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('account_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='supplymanagers', to='banking.accountdetail')),
                ('supply_business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.supplier')),
            ],
            bases=('core.user',),
        ),
    ]
