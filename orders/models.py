from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class DeliveryAgent(User):  # type: ignore
    # Choices
    VEHICLE_TYPE_CHOICE = [
        ('bicycle', _('Bicycle')),
        ('motorcycle', _('Motoroycle')),
        ('car', _('Car')),
        ('bus', _('Bus')),
        ('truck', _('Truck'))
    ]
    
    # Personal extended
    face_capture = models.ImageField(upload_to="images/profile_pic", blank=True, null=True)
    
    # Driving details
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICE, blank=True, null=True)
    vehicle_brand = models.CharField(max_length=256, blank=True, null=True)
    plate_number = models.CharField(max_length=10, blank=True, null=True)
    drivers_license = models.FileField(upload_to="images/drivers_license", null=True, blank=True)
    drivers_license_id = models.CharField(max_length=20, null=True, blank=True)
    voters_card = models.FileField(upload_to="images/voters_card", null=True, blank=True)
    voters_number = models.CharField(max_length=12, null=True, blank=True)
    nin_doc = models.FileField(upload_to="images/NIN_doc", null=True, blank=True)
    nin_number = models.CharField(max_length=11, null=True, blank=True)
    
    # Next of kin details
    N_O_N_full_name = models.CharField(max_length=256, blank=True, null=True)
    N_O_N_phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name=_("next-of-kin's phone number"),
    )
    
    # Guarantor's details
    guarantor_first_name = models.CharField(max_length=20, blank=True, null=True)
    guarantor_last_name = models.CharField(max_length=20, blank=True, null=True)
    guarantor_phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name=_("Guarantor's phone number"),
    )
    guarantor_occupation = models.CharField(max_length=30, blank=True, null=True)
    
    address = models.ForeignKey(
        "cities_light.Country", on_delete=models.SET_NULL, null=True, blank=True
    )
    # Fields
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    # last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("orders_DeliveryAgent_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("orders_DeliveryAgent_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("orders_DeliveryAgent_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("orders_DeliveryAgent_htmx_delete", args=(self.pk,))
