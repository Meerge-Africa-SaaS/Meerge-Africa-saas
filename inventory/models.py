import uuid

from cities_light.models import City
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("inventory_Category_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("inventory_Category_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("inventory_Category_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("inventory_Category_htmx_delete", args=(self.pk,))


class Item(models.Model):
    # Relationships
    category = models.ForeignKey("inventory.Category", on_delete=models.DO_NOTHING)
    supplier = models.ForeignKey("inventory.Supplier", on_delete=models.CASCADE)

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    unit_of_measure = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    expiry_date = models.DateField()

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("inventory_Item_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("inventory_Item_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("inventory_Item_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("inventory_Item_htmx_delete", args=(self.pk,))


class Stock(models.Model):
    # Relationships
    item = models.ForeignKey("inventory.Item", on_delete=models.DO_NOTHING)

    # Fields
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("inventory_Stock_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("inventory_Stock_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("inventory_Stock_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("inventory_Stock_htmx_delete", args=(self.pk,))


class Supplier(models.Model):
    # Relationships
    # city = models.ManyToManyField("world.City")
    city = models.ManyToManyField(
        City
    )  # , on_delete=models.SET_NULL, null=True, blank=True

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("inventory_Supplier_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("inventory_Supplier_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("inventory_Supplier_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("inventory_Supplier_htmx_delete", args=(self.pk,))


class SupplyManager(User):
    # Relationships
    supplier = models.ForeignKey("inventory.Supplier", on_delete=models.CASCADE)

    # Fields
    # last_updated = models.DateTimeField(auto_now=True, editable=False)
    # created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("inventory_SupplyManager_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("inventory_SupplyManager_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("inventory_SupplyManager_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("inventory_SupplyManager_htmx_delete", args=(self.pk,))
