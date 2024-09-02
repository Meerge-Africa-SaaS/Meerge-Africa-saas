# custom_adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.urls import reverse

from restaurants.models import Staff


class CustomAccountAdapter(DefaultAccountAdapter):
    
    def get_from_email(self):
        return "Meerge Africa"
    
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        user = emailconfirmation.email_address.user
        
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
    
    def get_reset_password_from_key_url(self, key):
        print(key)