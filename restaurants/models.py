import uuid

from cities_light.models import City, Country
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from invitations.base_invitation import AbstractBaseInvitation
from invitations.app_settings import app_settings
from invitations.adapters import get_invitations_adapter
import datetime

from django.contrib.sites.shortcuts import get_current_site

from django.utils import timezone
from django.utils.crypto import get_random_string

from invitations import signals

User = get_user_model()


class StaffInvitation(AbstractBaseInvitation):
    ROLE_CHOICES = [
        ("chef", "Chef"),
        ("sous_chef", "Sous Chef"),
        ("line_cook", "Line Cook"),
        ("restaurant_manager", "Restaurant Manager"),
        ("cashier", "Cashier"),
        ("assistant_restaurant_manager", "Assistant Restaurant Manager"),
        ("host", "Host"),
        ("kitchen_porter", "Kitchen Porter"),
        ("server", "Server"),
        ("dish_washer", "Dish Washer"),
    ]
    email = models.EmailField(
        unique=True,
        verbose_name=_("email address"),
    )
    role = models.CharField(max_length=28, choices=ROLE_CHOICES, blank=True, null=True)
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", on_delete=models.CASCADE, blank=True, null=True
    )
    created = models.DateTimeField(verbose_name=_("created"), default=timezone.now)

    @classmethod
    def create(
        cls,
        email: str,
        inviter: User,  # type: ignore
        role: str,
        restaurant: "Restaurant",
        **kwargs,
    ):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email,
            key=key,
            inviter=inviter,
            role=role,
            restaurant=restaurant,
            **kwargs,
        )
        return instance

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY,
        )
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        current_site = get_current_site(request)
        invite_url = reverse(app_settings.CONFIRMATION_URL_NAME, args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        role = self.role
        for r in self.ROLE_CHOICES:
            if r[0] == self.role:
                role = r[1]
                break

        ctx.update(
            {
                "invite_url": invite_url,
                "site_name": current_site.name,
                "email": self.email,
                "key": self.key,
                "inviter": self.inviter,
                "role": role,
                "restaurant": self.restaurant.name,
            },
        )

        email_template = "invitations/email/email_invite"

        get_invitations_adapter().send_mail(email_template, self.email, ctx)
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=self.inviter,
            role=self.role,
            restaurant=self.restaurant,
        )

    def __str__(self):
        return f"Invite: {self.email}"


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
    description = models.CharField(max_length=256, blank=True, null=True)
    date_time_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_time_updated = models.DateTimeField(auto_now=True, editable=False)
    date_from = models.DateField()
    date_to = models.DateField()
    category_ID = models.UUIDField(default=uuid.uuid4)

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
    category = models.ForeignKey(
        "restaurants.MenuCategory", on_delete=models.DO_NOTHING
    )
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
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE)

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
    STATUS_CHOICES = [("available", "Available"), ("unlisted", "Unlisted")]

    DIET_TYPE_CHOICES = [
        ("vegan", "VEGAN"),
        ("gluten_free", "GLUTEN FREE"),
        ("low_carbs", "LOW CARBS"),
        ("keto", "KETO"),
        ("lactose_free", "LACTOSE FREE"),
    ]

    SPICE_LEVEL_CHOICES = [("mild", "Mild"), ("medium", "Medium"), ("hot", "Hot")]

    # Relationships
    menu = models.ForeignKey("restaurants.Menu", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", models.CASCADE, related_name="menu_items"
    )
    add_ons = models.ManyToManyField(
        "restaurants.AddOn", related_name="menu_items", blank=True
    )
    ingredient_details = models.ManyToManyField("restaurants.Ingredient")

    # Fields
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    portion = models.IntegerField(blank=True, null=True)
    size = models.IntegerField()
    diet_type = models.CharField(
        max_length=12, choices=DIET_TYPE_CHOICES, blank=True, null=True
    )
    spice_level = models.CharField(
        max_length=6, choices=SPICE_LEVEL_CHOICES, blank=True, null=True
    )
    status = models.CharField(max_length=9, choices=STATUS_CHOICES)
    nutritional_info_summary = models.CharField(max_length=256, blank=True, null=True)
    ready_in = models.TimeField(blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    # image = models.ImageField(upload_to='images/restaurant/Menu/MenuItem')
    # video = models.FileField(upload_to='video/Menu/MenuItem')

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


class RestaurantStock(models.Model):
    # Relationships
    category = models.ForeignKey("inventory.Category", on_delete=models.DO_NOTHING, related_name="stocks")
    store = models.ForeignKey("restaurants.RestaurantStore", on_delete=models.CASCADE, related_name="stocks")
    #restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE, related_name="stocks")

    # Fields
    name = models.CharField(max_length=128)
    image = models.URLField(blank=True, null=True)
    # image = models.ImageField(upload_to='images/restaurant/Stock')
    stock_type = models.CharField(max_length=128)
    purchasing_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    measuring_unit = models.IntegerField()
    # manufacturers name = models.CharField(max_length = 128)
    # low_stock_alert_unit = models.DecimalField(max_digits=10, decimal_places = 2)
    # expiry_date = models.DateField()

    # Time
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def ready(self):
        pass

    class Meta:
        pass

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant_RestaurantStock_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_RestaurantStock_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_RestaurantStock_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_RestaurantStock_htmx_delete", args=(self.pk,))


class RestaurantCategory(models.Model):
    # Fields
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=256, blank=True, null=True)

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
    """CATEGORY_CHOICES = (
        ('cafe', _('Cafe')),
        ('bar', _('Bar')),
        ('lounge', _('Lounge')),
        ('hotel', _('Hotel')),
        ('food_joint', _('Food Joint')),
        ('street_vendor', _('Street Vendor'))
    )"""

    BUSINESS_REGISTRATION_CHOICE = (
        ("registered", _("Registered")),
        ("unregistered", _("Unregistered")),
    )

    # Relationships
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    owner = models.ManyToManyField("core.User", related_name="restaurant_owner")
    business_category = models.ManyToManyField(
        "restaurants.RestaurantCategory", related_name="restaurants"
    )
    add_ons = models.ManyToManyField(
        "restaurants.AddOn", related_name="restaurant_add_ons", blank=True
    )

    # Fields
    address = models.CharField(max_length=130)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name=_("email address"), max_length=256, unique=True
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
    business_reg_details = models.CharField(
        max_length=12, choices=BUSINESS_REGISTRATION_CHOICE
    )
    cac_reg_number = models.CharField(max_length=20, null=True, blank=True)
    cac_certificate = models.URLField(blank=True, null=True)
    business_license = models.URLField(blank=True, null=True)
    # cac_certificate = models.FileField(upload_to="images/restaurant/cac_certificates")
    # business_license = models.FileField(upload_to="images/restaurant/business_license", null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True, editable=False)
    profile_img = models.URLField(blank=True, null=True)
    cover_img = models.URLField(blank=True, null=True)
    # profile_img = models.ImageField(upload_to="images/restaurant/profile_images")
    # cover_img = models.ImageField(upload_to="images/restaurant/cover_images")

    # Miscellanous
    custom_link = models.SlugField(
        max_length=24,
        unique=True,
        help_text="Custom link for your restaurant URL",
        blank=True,
        null=True,
    )

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.custom_link = self.custom_link or slugify(self.name)
        super(Restaurant, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("restaurant_Restaurant_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_Restaurant_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_Restaurant_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_Restaurant_htmx_delete", args=(self.pk,))


class RestaurantStore(models.Model):
    # Relationships
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE, related_name="stores")

    # Fields
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    # image = models.ImageField(upload_to='images/restaurant/Store')
    section_name = models.CharField(max_length=128, blank=True, null=True)

    # Time
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant_RestaurantStore_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("restaurant_RestaurantStore_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("restaurant_RestaurantStore_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("restaurant_RestaurantStore_htmx_delete", args=(self.pk,))


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
