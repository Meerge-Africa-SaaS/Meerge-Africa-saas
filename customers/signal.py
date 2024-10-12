from django.db.models.signals import post_save
from models import Order


def send_delivery_request(self, instance, create, **kwargs):
     if created:
         pass
         #delivery_request = 