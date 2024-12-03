from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ninja import Form

from phonenumber_field.modelfields import PhoneNumberField
from customers.models import Order
from banking.models import AccountDetail
import uuid

User = get_user_model()


class DeliveryRequest(models.Model):
    
    # Choices
    STATUS_CHOICE = [
        ('pending', _('Pending')),
        ('assigned', _('Assigned')),
        ('processing', _('Processing')),
        ('completed', _('Completed'))
    ]
    
    # Relationships
    order = models.ForeignKey('customers.Order', on_delete=models.DO_NOTHING)
    deliveryagent = models.ForeignKey('orders.DeliveryAgent', on_delete=models.DO_NOTHING, null=True, blank=True)
     
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=12, choices=STATUS_CHOICE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        db_table = "deliveryrequest"

    def __str__(self):
        return f"Delivery Request for Order {self.order.id}"

    def get_absolute_url(self):
        return reverse("deliveryagentDeliveryRequest_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("deliveryagentDeliveryRequest_detail", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("deliveryagentDeliveryRequest_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("deliveryagentDeliveryRequest_delete", args=(self.pk,))
    
    #def save(self):
        

class DeliveryAgent(User):
    # Relationships
    account_details = models.ForeignKey(AccountDetail, related_name="deliveryagents", on_delete=models.DO_NOTHING, null=True, blank=True)
    
    # Fields
    # Choices
    VEHICLE_TYPE_CHOICE = [
        ('bicycle', _('Bicycle')),
        ('motorcycle', _('Motoroycle')),
        ('car', _('Car')),
        ('bus', _('Bus')),
        ('truck', _('Truck'))
    ]
    
    # Personal extended
    address = models.ForeignKey("cities_light.Country", on_delete=models.DO_NOTHING)
    terms_and_condition = models.BooleanField()
    face_capture = CloudinaryField("delivery_agent_face_capture", blank=True, null=True)
    #face_capture = models.ImageField(upload_to="images/profile_pic", null=True, blank=True)
    work_shift = models.JSONField(null=True, blank=True)
    
    # Driving details
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICE, null=True, blank=True)
    vehicle_brand = models.CharField(max_length=256, null=True, blank=True)
    plate_number = models.CharField(max_length=10, blank=True, null=True)
    drivers_license = CloudinaryField("delivery_agent_drivers_license", blank=True, null=True)
    #drivers_license = models.FileField(upload_to="images/drivers_license", null=True, blank=True)
    drivers_license_id = models.CharField(max_length=20, null=True, blank=True)
    voters_card = CloudinaryField("delivery_agent_voters_card", blank=True, null=True)
    #voters_card = models.FileField(upload_to="images/voters_card", null=True, blank=True)
    voters_number = models.CharField(max_length=12, null=True, blank=True)
    nin_doc = CloudinaryField("delivery_agent_nin_doc", blank=True, null=True)
    #nin_doc = models.FileField(upload_to="images/NIN_doc", null=True, blank=True)
    nin_number = models.CharField(max_length=11, null=True, blank=True)
    
    # Next of kin details
    N_O_N_full_name = models.CharField(max_length=256, null=True, blank=True)
    N_O_N_phone_number = PhoneNumberField(verbose_name=_("next-of-kin's phone number"), null=True, blank=True)
    
    # Guarantor's details
    guarantor_first_name = models.CharField(max_length=20, null=True, blank=True)
    guarantor_last_name = models.CharField(max_length=20, null=True, blank=True)
    guarantor_phone_number = PhoneNumberField(verbose_name=_("Guarantor's phone number"), null=True, blank=True)
    guarantor_occupation = models.CharField(max_length=30, null=True, blank=True)
    
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

''' 
class DeliveryRequest(models.Model):
    DELIVERY_REQUEST_STATUSES = [
        ("pending", _("Pending")),
        ("in_motion", _("On the way")),
        ("delivered", _("Delivered"))
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(choices=DELIVERY_REQUEST_STATUSES, max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Delivery Request for Order {order.id}"
    
    
    def save(self):
        super().__init__()
        from .signals import delivery_request_created
        delivery_request_created.send(sender = self.__class__, instance = instance, created = True)
 '''