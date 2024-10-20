import uuid

from cities_light.models import City
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

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
    category = models.ForeignKey(
        "inventory.Category", on_delete=models.DO_NOTHING
    )
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
    item = models.ForeignKey("inventory.Item", on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(
        auto_now=True, editable=False, blank=True, null=True
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, blank=True, null=True
    )
    SKU_number = models.CharField(max_length=60, blank=True, null=True)
    product_name = models.CharField(max_length=60, blank=True, null=True)
    product_image = models.ImageField(
        upload_to="images/restaurant/cover_images", default="path/to/default/image.jpg"
    )
    product_category = models.CharField(max_length=60, blank=True, null=True)
    manufacture_name = models.CharField(max_length=60, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit_available = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    AVAILABILITY_CHOICES = [
        ("pre_order", "Pre-order"),
        ("in_stock", "In-stock"),
        ("out_of_stock", "Out of stock"),
    ]
    discount_percentage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    DELIVERY_CHOICES = [
        ("same_day", "Same day (Orders before 12 noon)"),
        ("number_of_days", "Number of days"),
    ]
    pickup_available = models.BooleanField(
        default=False, verbose_name="Pickup Available", blank=True, null=True
    )

    class Meta:
        pass

    def _str_(self):
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
    # Choices
    SUPPLIER_CATEGORY = [
        ("sea_food", "Sea Food"),
        ("vegetables", "Vegetables"),
        ("meat_and_poultry", "Meat and Poultry"),
        ("grains", "Grain Products"),
        ("soup_and_condiments", "Soups and Condiments"),
        ("spices_and_seasoning", "Spices and Seasoning"),
        ("oil_and_fat", "Oil and Fat"),
        ("baking_products", "Baking Products"),
        ("fruits_and_nuts", "Fruits and Nuts"),
        ("diary_products", "Diary Products"),
        ("spread_and_sweeteners", "Spread and Sweeteners"),
        ("drinks_and_beverages", "Drinks and Beverages")
    ]
    # Relationships
    # city = models.ManyToManyField("world.City")
    city = models.ManyToManyField(
        City
    )  # , on_delete=models.SET_NULL, null=True, blank=True
    owner = models.ForeignKey('core.User', on_delete=models.CASCADE)

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    cac_reg_number = models.CharField(max_length = 20, null=True, blank=True)
    cac_certificate = models.FileField(upload_to="images/supplier/cac_certificates")
    business_license = models.FileField(upload_to="images/supplier/business_license", null=True, blank=True)
    category = models.CharField(choices=SUPPLIER_CATEGORY, max_length = 21)
    
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    profile_img = models.ImageField(upload_to="images/restaurant/profile_images")
    cover_img = models.ImageField(upload_to="images/restaurant/cover_images")

    address = models.CharField(max_length=130)

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


class SupplyManager(User):  # type: ignore
    # Relationships
    supply_business = models.ForeignKey("inventory.Supplier", on_delete=models.CASCADE)

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

class Store(models.Model):
    name = models.CharField(max_length=255)
    business_section_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    store_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
