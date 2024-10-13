''' from django.db.models.signals import Signal
delivery_request_created = Signal(providing_args=["instance", "created"]) '''


from django.db.models.signals import post_save
from customers.models import Order
from .models import DeliveryRequest


def send_delivery_request(self, instance, created, **kwargs):
     if created:
         delivery_request = DeliveryRequest.objects.create(order=instance, status='pending')
         print("Delivery Request has been created")
         
post_save.connect(send_delivery_request, sender=Order)