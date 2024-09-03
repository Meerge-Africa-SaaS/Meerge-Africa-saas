import uuid

from cities_light.models import City, Country
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class Order(models.Model):

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_address = models.CharField(max_length=130)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'orders'

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


class Customer(User):

    # Relationships
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    # Fields
    # last_name = models.CharField(max_length=30)
    # last_updated = models.DateTimeField(auto_now=True, editable=False)
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    address = models.CharField(max_length=130)
    # first_name = models.CharField(max_length=30)

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
