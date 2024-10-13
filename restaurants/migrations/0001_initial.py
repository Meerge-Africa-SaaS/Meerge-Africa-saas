# Generated by Django 5.0.6 on 2024-10-12 18:17

import django.db.models.deletion
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('core', '0001_initial'),
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddOn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('add_on_ID', models.UUIDField(default=uuid.uuid4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('date_time_updated', models.DateTimeField(auto_now=True)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('category_ID', models.UUIDField(default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('date_to', models.DateField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurants.menucategory')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('portion', models.IntegerField(blank=True, null=True)),
                ('size', models.IntegerField()),
                ('diet_type', models.CharField(blank=True, choices=[('vegan', 'VEGAN'), ('gluten_free', 'GLUTEN FREE'), ('low_carbs', 'LOW CARBS'), ('keto', 'KETO'), ('lactose_free', 'LACTOSE FREE')], max_length=12, null=True)),
                ('spice_level', models.CharField(blank=True, choices=[('mild', 'Mild'), ('medium', 'Medium'), ('hot', 'Hot')], max_length=6, null=True)),
                ('status', models.CharField(choices=[('available', 'Available'), ('unlisted', 'Unlisted')], max_length=9)),
                ('nutritional_info_summary', models.CharField(blank=True, max_length=256, null=True)),
                ('ready_in', models.TimeField(blank=True, null=True)),
                ('discount_percentage', models.PositiveIntegerField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='images/restaurant/Menu/MenuItem')),
                ('video', models.FileField(upload_to='video/Menu/MenuItem')),
                ('menu_item_ID', models.UUIDField(default=uuid.uuid4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('add_ons', models.ManyToManyField(blank=True, related_name='menu_items', to='restaurants.addon')),
                ('ingredient_details', models.ManyToManyField(to='restaurants.ingredient')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.menu')),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='menu_item',
            field=models.ManyToManyField(to='restaurants.menuitem'),
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=130)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=256, unique=True, verbose_name='email address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, error_messages={'unique': 'A restaurant with that phone number already exists.'}, max_length=128, null=True, region=None, unique=True, verbose_name='phone number')),
                ('business_reg_details', models.CharField(choices=[('registered', 'Registered'), ('unregistered', 'Unregistered')], max_length=12)),
                ('cac_reg_number', models.CharField(blank=True, max_length=20, null=True)),
                ('cac_certificate', models.FileField(upload_to='images/restaurant/cac_certificates')),
                ('business_license', models.FileField(blank=True, null=True, upload_to='images/restaurant/business_license')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('profile_img', models.ImageField(upload_to='images/restaurant/profile_images')),
                ('cover_img', models.ImageField(upload_to='images/restaurant/cover_images')),
                ('custom_link', models.SlugField(blank=True, help_text='Custom link for your restaurant URL', max_length=24, null=True, unique=True)),
                ('add_ons', models.ManyToManyField(blank=True, related_name='restaurant_add_ons', to='restaurants.addon')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.country')),
                ('owner', models.ManyToManyField(related_name='restaurant_owner', to=settings.AUTH_USER_MODEL)),
                ('business_category', models.ManyToManyField(related_name='restaurants', to='restaurants.restaurantcategory')),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='restaurants.restaurant'),
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
        migrations.AddField(
            model_name='addon',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
        migrations.CreateModel(
            name='RestaurantStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to='images/restaurant/Stock')),
                ('stock_type', models.CharField(max_length=128)),
                ('purchasing_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('measuring_unit', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.category')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('image', models.ImageField(upload_to='images/restaurant/Store')),
                ('section_name', models.CharField(blank=True, max_length=128, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(blank=True, choices=[('chef', 'Chef'), ('sous_chef', 'Sous Chef'), ('line_cook', 'Line Cook'), ('restaurant_manager', 'Restaurant Manager'), ('cashier', 'Cashier'), ('assistant_restaurant_manager', 'Assistant Restaurant Manager'), ('host', 'Host'), ('kitchen_porter', 'Kitchen Porter'), ('server', 'Server'), ('dish_washer', 'Dish Washer')], max_length=28, null=True)),
                ('restaurants', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
            options={
                'verbose_name_plural': 'Staff',
            },
            bases=('core.user',),
        ),
        migrations.CreateModel(
            name='AssistantRestaurantManager',
            fields=[
            ],
            options={
                'verbose_name': 'Assistant Restaurant Manager',
                'verbose_name_plural': 'Assistant Restaurant Managers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='Cashier',
            fields=[
            ],
            options={
                'verbose_name': 'Cashier',
                'verbose_name_plural': 'Cashiers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
            ],
            options={
                'verbose_name': 'Chef',
                'verbose_name_plural': 'Chefs',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='DishWasher',
            fields=[
            ],
            options={
                'verbose_name': 'Dish Washer',
                'verbose_name_plural': 'Dish Washers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'Hosts',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='KitchenPorter',
            fields=[
            ],
            options={
                'verbose_name': 'Kitchen Porter',
                'verbose_name_plural': 'Kitchen Porters',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='LineCook',
            fields=[
            ],
            options={
                'verbose_name': 'Line Cook',
                'verbose_name_plural': 'Line Cooks',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='RestaurantManager',
            fields=[
            ],
            options={
                'verbose_name': 'Restaurant Manager',
                'verbose_name_plural': 'Restaurant Managers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
            ],
            options={
                'verbose_name': 'Server',
                'verbose_name_plural': 'Servers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
        migrations.CreateModel(
            name='SousChef',
            fields=[
            ],
            options={
                'verbose_name': 'Sous Chef',
                'verbose_name_plural': 'Sous Chefs',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('restaurants.staff',),
        ),
    ]
