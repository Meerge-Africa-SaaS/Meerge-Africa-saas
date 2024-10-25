import uuid
from phonenumber_field.modelfields import PhoneNumberField

from cities_light.models import City, Country
from banking.models import AccountDetail
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Order(models.Model):
    # Relationships
    customer = models.ForeignKey('customers.Customer', on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.DO_NOTHING)
    menu_item = models.ForeignKey('restaurants.MenuItem', on_delete=models.DO_NOTHING)
    add_on = models.ForeignKey('restaurants.AddOn', on_delete=models.DO_NOTHING, blank=True, null=True)
    
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_address = models.CharField(max_length=130)
    driver_note = models.CharField(max_length=256, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("customers_Order_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("customers_Order_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("customers_Order_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("customers_Order_htmx_delete", args=(self.pk,))


class Customer(User):  # type: ignore
    # Relationships
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    account_details = models.ForeignKey(AccountDetail, related_name="customers", on_delete=models.DO_NOTHING, null=True, blank=True)

    # Fields
    alt_phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name=_("phone number"),)
    allergies = models.CharField(max_length=250, blank=True, null=True)
    first_time_food_tryouts = models.CharField(max_length=250, blank=True, null=True)
    healthy_diet_goals = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=130)
    # last_updated = models.DateTimeField(auto_now=True, editable=False)
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    
    

    class Meta:
        db_table = "customers"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("customers_Customer_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("customers_Customer_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("customers_Customer_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("customers_Customer_htmx_delete", args=(self.pk,))


