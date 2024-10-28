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
    ''' 
    def get_email_confirmation_url(self, request, emailconfirmation):
        
        url = f'http://localhost:8000/test/{emailconfirmation.key}/'
        return url

    
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
     '''
    
    ''' def get_email_confirmation_url(self, request, emailconfirmation):
        #return 
        pass '''
