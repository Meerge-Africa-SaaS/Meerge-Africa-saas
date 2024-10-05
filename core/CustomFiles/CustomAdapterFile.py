# custom_adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.urls import reverse

from restaurants.models import Staff
<<<<<<< HEAD
=======
from inventory.models import SupplyManager
from customers.model import Customer
from orders.model import DeliveryAgent
>>>>>>> MA-183-Create-Add-Menu-Item-Endpoint-for-Chef-Restaurant-Owner-Meerge


class CustomAccountAdapter(DefaultAccountAdapter):
    
    def get_from_email(self):
        return "Meerge Africa"
    
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        user = emailconfirmation.email_address.user
<<<<<<< HEAD
        
        is_staff = isinstance(user, Staff)
        actor_type = "staff" if is_staff else ""
        
        if isinstance(user, Staff) == False:
            actor_type = "owner"
        print("ACTOR TYPE IS ", actor_type)
        if (actor_type == "staff" or actor_type == "owner"):
            url = f"{settings.ACCOUNT_EMAIL_CONFIRMATION_URL}{key}"
        else:
            pass
        
        return url

=======
                
        if isinstance(user, Customer):
            actor_type = "customer"
        elif isinstance(user, Staff):
            actor_type = "staff"
        elif isinstance(user, SupplyManager):
            actor_type = "supplymanager"
        if not (isinstance(user, Staff)) and not (isinstance(user, SupplyManager)) and not (isinstance(user, DeliveryAgent)) and not (isinstance(user, Customer)):
            actor_type = "owner"
            
        if isinstance(user, Customer) or isinstance(user, DeliveryAgent):
            url = f"{settings.ACCOUNT_EMAIL_CONFIRMATION_URL}/mobile/{key}"
        else:
            f"{settings.ACCOUNT_EMAIL_CONFIRMATION_URL}/mobile/{key}"
        
        return url
    
    def get_reset_password_url(self, request):
            url = "Hallo"
            print(url)
            return url
    
    def get_reset_password_from_key_url(self, key):
        print("\n"*5, key, "\n"*5)
>>>>>>> MA-183-Create-Add-Menu-Item-Endpoint-for-Chef-Restaurant-Owner-Meerge
