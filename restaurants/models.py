from cities_light.models import City, Country
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

import uuid

User = get_user_model()


class Ingredient(models.Model):
    # Relationships
    menu_item = models.ManyToManyField("restaurants.MenuItem")

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("restaurant_Ingredient_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Ingredient_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Ingredient_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Ingredient_htmx_delete", args=(self.pk,))


class MenuCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length = 256, blank = True, null = True)
    date_time_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_time_updated = models.DateTimeField(auto_now= True, editable=False)
    date_from = models.DateField()
    date_to = models.DateField()
    category_ID = models.UUIDField(default = uuid.uuid4)
    
    class Meta:
        pass
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("menuCategory_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("menuCategory_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("menuCategory_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("menuCategory_htmx_delete", args=(self.pk,))


class Menu(models.Model):
    # Relationships
    category = models.ForeignKey("restaurants.MenuCategory", on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE)
    
    # Fields
    date_from = models.DateField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    date_to = models.DateField()
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("restaurant_Menu_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Menu_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Menu_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Menu_htmx_delete", args=(self.pk,))


class AddOn(models.Model):
    # Relationships
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
    
    # Fields
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    add_on_ID = models.UUIDField(default=uuid.uuid4)
    
    # Time
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    
    
    class Meta:
        pass
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("restaurant_MenuItem_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_MenuItem_update", args=(self.pk,))
    


class MenuItem(models.Model):
    # Choices
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unlisted', 'Unlisted')
    ]
    
    DIET_TYPE_CHOICES = [
        ('vegan', 'VEGAN'),
        ('gluten_free', 'GLUTEN FREE'),
        ('low_carbs', 'LOW CARBS'),
        ('keto', 'KETO'),
        ('lactose_free', 'LACTOSE FREE')
    ]
    
    SPICE_LEVEL_CHOICES = [
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('hot', 'Hot')
    ]
    
    # Relationships
    menu = models.ForeignKey("restaurants.Menu", on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurants.Restaurant', models.CASCADE)
    add_ons = models.ManyToManyField('restaurants.AddOn', related_name='menu_items', blank=True)
    ingredient_details = models.ManyToManyField('restaurants.Ingredient')

    # Fields
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    portion = models.IntegerField(blank=True, null=True)
    size = models.IntegerField()
    diet_type = models.CharField(max_length = 12, choices=DIET_TYPE_CHOICES, blank=True, null=True)
    spice_level =  models.CharField(max_length = 6, choices=SPICE_LEVEL_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES)
    nutritional_info_summary = models.CharField(max_length = 256, blank=True, null=True)
    ready_in = models.TimeField(blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='images/restaurant/Menu/MenuItem')
    video = models.FileField(upload_to='video/Menu/MenuItem')
    
    # Miscellenous
    menu_item_ID = models.UUIDField(default=uuid.uuid4)
    
    # Time
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("restaurant_MenuItem_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_MenuItem_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_MenuItem_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_MenuItem_htmx_delete", args=(self.pk,))


class RestaurantCategory(models.Model):
    
    # Fields
    name = models.CharField(max_length=20)
    description =  models.CharField(max_length=256, blank=True, null=True)
    
    class Meta:
        pass
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant_RestaurantCategory_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_RestaurantCategory_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_RestaurantCategory_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_RestaurantCategory_htmx_delete", args=(self.pk,))
    


class Restaurant(models.Model):
    ''' CATEGORY_CHOICES = (
        ('cafe', _('Cafe')),
        ('bar', _('Bar')),
        ('lounge', _('Lounge')),
        ('hotel', _('Hotel')),
        ('food_joint', _('Food Joint')),
        ('street_vendor', _('Street Vendor'))        
    ) '''
    
    BUSINESS_REGISTRATION_CHOICE = (
        ('registered', _("Registered")),
        ('unregistered', _("Unregistered"))
    )
    
    # Relationships
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    owner = models.ManyToManyField("core.User")
    business_category = models.ManyToManyField('restaurants.RestaurantCategory', related_name='restaurants')

    # Fields
    address = models.CharField(max_length=130)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=256,
        unique=True
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("phone number"),
        error_messages={
            "unique": _("A restaurant with that phone number already exists."),
        },
    )
    business_reg_details = models.CharField(max_length=12,choices=BUSINESS_REGISTRATION_CHOICE)
    cac_reg_number = models.CharField(max_length=20, null=True, blank=True)
    cac_certificate = models.FileField(upload_to="images/restaurant/cac_certificates")
    business_license = models.FileField(upload_to="images/restaurant/business_license", null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True, editable=False)
    profile_img = models.ImageField(upload_to="images/restaurant/profile_images")
    cover_img = models.ImageField(upload_to="images/restaurant/cover_images")
    
    # Miscellanous
    add_ons = models.ManyToManyField('restaurants.AddOn', related_name='restaurant_add_ons', blank=True)

    
    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("restaurant_Restaurant_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Restaurant_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Restaurant_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Restaurant_htmx_delete", args=(self.pk,))


""" 
class Chef(User):

    # Relationships
    #restaurants = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE)

    # Fields
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    # last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("restaurant_Chef_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Chef_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Chef_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Chef_htmx_delete", args=(self.pk,))

 """


class Staff(User):  # type: ignore
    role_choices = (
        ("chef", _("Chef")),
        ("sous_chef", _("Sous Chef")),
        ("line_cook", _("Line Cook")),
        ("restaurant_manager", _("Restaurant Manager")),
        ("cashier", _("Cashier")),
        ("assistant_restaurant_manager", _("Assistant Restaurant Manager")),
        ("host", _("Host")),
        ("kitchen_porter", _("Kitchen Porter")),
        ("server", _("Server")),
        ("dish_washer", _("Dish Washer")),
    )

    # Fields
    role = models.CharField(max_length=28, choices=role_choices, blank=True, null=True)
    # Relationships
    restaurants = models.ForeignKey(
        "restaurants.Restaurant", on_delete=models.CASCADE, blank=True, null=True
    )

    # Fields
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    # last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("restaurant_Staff_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Staff_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Staff_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Staff_htmx_delete", args=(self.pk,))


"""
    The models below are the proxy models that are linked to the staff models.
    No need to create a separate model for every staff-type.
"""


class RestaurantManager(Staff):
    objects = Staff.objects.filter(role="restaurant_manager")

    class Meta:
        proxy = True
        verbose_name = "Restaurant Manager"
        verbose_name_plural = "Restaurant Managers"

    def works_at(self):
        return f"{self.email} manages {self.restaurants}"


class AssistantRestaurantManager(Staff):
    objects = Staff.objects.filter(role="assistant_restaurant_manager")

    class Meta:
        proxy = True
        verbose_name = "Assistant Restaurant Manager"
        verbose_name_plural = "Assistant Restaurant Managers"

    def works_at(self):
        return f"{self.email} assists restaurant manager at {self.restaurants}"


class Chef(Staff):
    objects = Staff.objects.filter(role="chef")

    class Meta:
        proxy = True
        verbose_name = "Chef"
        verbose_name_plural = "Chefs"

    def works_at(self):
        return f"{self.email} works at {self.restaurants}"


class SousChef(Staff):
    objects = Staff.objects.filter(role="sous_chef")

    class Meta:
        proxy = True
        verbose_name = "Sous Chef"
        verbose_name_plural = "Sous Chefs"

    def works_at(self):
        return f"{self.email} works at {self.restaurants}"


class LineCook(Staff):
    objects = Staff.objects.filter(role="line_cook")

    class Meta:
        proxy = True
        verbose_name = "Line Cook"
        verbose_name_plural = "Line Cooks"

    def works_at(self):
        return f"{self.email} works at {self.restaurants}"


class Host(Staff):
    objects = Staff.objects.filter(role="host")

    class Meta:
        proxy = True
        verbose_name = "Host"
        verbose_name_plural = "Hosts"

    def works_at(self):
        return f"{self.email} works at {self.restaurants}"


class Cashier(Staff):
    objects = Staff.objects.filter(role="cashier")

    class Meta:
        proxy = True
        verbose_name = "Cashier"
        verbose_name_plural = "Cashiers"

    def works_at(self):
        return f"{self.email} works at {self.restaurants}"


class KitchenPorter(Staff):
    objects = Staff.objects.filter(role="kitchen_porter")

    class Meta:
        proxy = True
        verbose_name = "Kitchen Porter"
        verbose_name_plural = "Kitchen Porters"

    def works_at(self):
        return f"{self.email} works at {self.restaurants}"


class Server(Staff):
    objects = Staff.objects.filter(role="server")

    class Meta:
        proxy = True
        verbose_name = "Server"
        verbose_name_plural = "Servers"

    def works_at(self):
        return f"{self.email} works at {self.restaurants}"


class DishWasher(Staff):
    objects = Staff.objects.filter(role="dish_washer")

    class Meta:
        proxy = True
        verbose_name = "Dish Washer"
        verbose_name_plural = "Dish Washers"

    def works_at(self):
        return f"{self.email} works at {self.restaurants}"
