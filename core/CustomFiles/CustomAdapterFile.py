# custom_adapter.py
import os

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from restaurants.models import Staff
from inventory.models import SupplyManager
from customers.models import Customer
from orders.models import DeliveryAgent

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from allauth.account.signals import user_signed_up

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # current_site = request.site
        user = emailconfirmation.email_address.user
        if "owner" in [g.name.lower() for g in user.groups.all()]:
            user_type = "owner"
        # Choose template based on user type
        template_prefix = {
            'owner': 'emails/owner',
            'type2': 'emails/type2',
            'type3': 'emails/type3',
            'type4': 'emails/type4',
        }.get(user_type, '../templates/emails/default')

        ctx = {
            "user": user,
            "activate_url": self.get_email_confirmation_url(request, emailconfirmation),
            # "current_site": current_site,
            # "current_site": get_current_site(globals()["context"].request),
            "key": emailconfirmation.key,
        }

        subject = render_to_string(f'{template_prefix}_subject.txt', ctx)
        subject = " ".join(subject.splitlines()).strip()
        body = render_to_string(f'{template_prefix}_message.txt', ctx)

        email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [emailconfirmation.email_address.email])
        email.send()

    def is_open_for_signup(self, request):
        return True

    def get_user_signed_up_signal(self):
        return user_signed_up

    def get_from_email(self):
        return os.getenv("EMAIL_HOST_USER", "account@meergeafrica.com")
    
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
