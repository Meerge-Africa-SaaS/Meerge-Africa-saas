from cities_light.models import City, Country
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

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


class Menu(models.Model):
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


class MenuItem(models.Model):
    # Relationships
    menu = models.ForeignKey("restaurants.Menu", on_delete=models.CASCADE)

    # Fields
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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


class Restaurant(models.Model):
    CATEGORY_CHOICES = (
        ('cafe', _('Cafe')),
        ('bar', _('Bar')),
        ('lounge', _('Lounge')),
        ('hotel', _('Hotel')),
        ('food_joint', _('Food Joint')),
        ('street_vendor', _('Street Vendor'))        
    )
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
    #business_category = model
    business_reg_details = models.CharField(max_length=12,choices=BUSINESS_REGISTRATION_CHOICE)
    cac_reg_number = models.CharField(max_length = 20, null=True, blank=True)
    cac_certificate = models.FileField(upload_to="images/restaurant/cac_certificates")
    business_license = models.FileField(upload_to="images/restaurant/business_license", null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True, editable=False)
    profile_img = models.ImageField(upload_to="images/restaurant/profile_images")
    cover_img = models.ImageField(upload_to="images/restaurant/cover_images")

    
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
