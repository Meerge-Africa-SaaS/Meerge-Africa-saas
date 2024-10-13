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
    
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        user = emailconfirmation.email_address.user

                
        if isinstance(user, Customer):
            actor_type = "customer"
        elif isinstance(user, Staff):
            actor_type = "staff"
        elif isinstance(user, SupplyManager):
            actor_type = "supplymanager"
        elif isinstance(user, DeliveryAgent):
            actor_type = "deliveryagent"
        else:
            actor_type = "owner"
    

        if actor_type == "customer" or actor_type == "deliveryagent":
            url = f"{settings.ACCOUNT_EMAIL_CONFIRMATION_URL}/mobile/{key}"
        else:
            url = f"{settings.ACCOUNT_EMAIL_CONFIRMATION_URL}/{key}"
        
        return url
    
    def get_reset_password_url(self, request):
            url = "Hallo"
            print(url)
            return url
    
    def get_reset_password_from_key_url(self, key):
        print("\n"*5, key, "\n"*5)
