# custom_adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.urls import reverse

from restaurants.models import Staff
from inventory.models import SupplyManager
from customers.models import Customer
from orders.models import DeliveryAgent


class CustomAccountAdapter(DefaultAccountAdapter):
    
    def get_from_email(self):
        return "account@meergeafrica.com"
    
    def get_email_verification_redirect_url(self, email_address):
        return reverse("actor_redirect")
    
    def get_reset_password_url(self, request):
            url = "Hallo"
            print(url)
            return url
    
    def get_reset_password_from_key_url(self, key):
        print("\n"*5, key, "\n"*5)
