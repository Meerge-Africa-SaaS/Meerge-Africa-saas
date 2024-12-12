import uuid
from cloudinary.models import CloudinaryField

from cities_light.models import City
from banking.models import AccountDetail
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = "Categories"

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


class ItemCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = "Item Categories"

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("inventory_ItemCategory_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("inventory_ItemCategory_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("inventory_ItemCategory_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("inventory_ItemCategory_htmx_delete", args=(self.pk,))


class Item(models.Model):
    category = models.ForeignKey("inventory.ItemCategory", on_delete=models.DO_NOTHING)
    stock = models.ForeignKey("inventory.Stock", on_delete=models.CASCADE, null=True)

    last_updated = models.DateTimeField(auto_now=True, editable=False)
    unit_of_measure = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    expiry_date = models.DateField()

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
    supplier = models.ForeignKey("inventory.Supplier", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    SKU_number = models.CharField(max_length=60, blank=True, null=True)
    product_name = models.CharField(max_length=60, blank=True, null=True)
    product_image = models.URLField(blank=True, null=True)
    # product_image = models.ImageField(upload_to="images/restaurant/cover_images", default="path/to/default/image.jpg")
    product_image = CloudinaryField("inventory_stocks")
    #product_image = models.ImageField(upload_to="images/restaurant/cover_images", default="path/to/default/image.jpg")
    product_category = models.CharField(max_length=60, blank=True, null=True)
    manufacture_name = models.CharField(max_length=60, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit_available = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )
    size = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )
    weight = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )
    discount_percentage = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )
    pickup_available = models.BooleanField(default=False, verbose_name="Pickup Available", blank=True, null=True)

    AVAILABILITY_CHOICES = [
        ("pre_order", "Pre-order"),
        ("in_stock", "In-stock"),
        ("out_of_stock", "Out of stock"),
    ]
    DELIVERY_CHOICES = [
        ("same_day", "Same day (Orders before 12 noon)"),
        ("number_of_days", "Number of days"),
    ]

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
    city = models.ManyToManyField(City, related_name="suppliers")
    owner = models.ForeignKey('core.User', on_delete=models.CASCADE)
    category = models.ManyToManyField('inventory.Category', related_name='suppliers')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=256,
        unique=True
    )
    phone_number = PhoneNumberField(
        blank=True, null=True, unique=True,
        verbose_name=_("phone number"),
        error_messages={"unique": _("A supplier with that phone number already exists.")},
    )
    cac_reg_number = models.CharField(max_length = 20, null=True, blank=True)
    cac_certificate = CloudinaryField("supplier_cac_certificates", blank=True, null=True)
    business_license = CloudinaryField("supplier_business_license", blank=True, null=True)
    #cac_certificate = models.FileField(upload_to="images/supplier/cac_certificates")
    #business_license = models.FileField(upload_to="images/supplier/business_license", null=True, blank=True)
    
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    profile_img = CloudinaryField("supplier_profile_image", blank=True, null=True)
    cover_img = CloudinaryField("supplier_cover_image", blank=True, null=True)
    #profile_img = models.ImageField(upload_to="images/restaurant/profile_images", blank=True, null=True)
    #cover_img = models.ImageField(upload_to="images/restaurant/cover_images", blank=True, null=True)

    address = models.CharField(max_length=130)

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
    supply_business = models.ForeignKey("inventory.Supplier", on_delete=models.CASCADE)
    account_details = models.ForeignKey(
        AccountDetail, related_name="supplymanagers", on_delete=models.DO_NOTHING, null=True, blank=True
    )

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=255)
    business_section_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    store_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
