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
        
        if (actor_type == "staff"):
            url = f"{settings.ACCOUNT_EMAIL_CONFIRMATION_URL}{key}"
        else:
            url = f"{settings.ACCOUNT_EMAIL_CONFIRMATION_URL}{key}"
        
        return url


''' 
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from restaurants.models import Staff

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        user = emailconfirmation.email_address.user
        is_staff = isinstance(user, Staff)
        user_type = 'staff' if is_staff else 'user'

        if request and not request.META.get('HTTP_X_MOBILE'):
            # Web user
            return f"{settings.SITE_URL}/{user_type}/confirm-email/{key}/"
        else:
            # Mobile user
            return f"your-app-scheme://{user_type}/confirm-email/{key}/"

    def render_mail(self, template_prefix, email, context):
        user = context.get('user')
        context['is_staff'] = isinstance(user, Staff)
        context['custom_message'] = "Thank you for registering!"
        return super().render_mail(template_prefix, email, context)

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = 'account/email/email_confirmation_signup'
        else:
            email_template = 'account/email/email_confirmation'
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
         '''
        