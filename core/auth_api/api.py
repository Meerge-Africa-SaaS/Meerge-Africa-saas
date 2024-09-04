from random import randint
import secrets
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.forms.models import model_to_dict

from ninja import Router
#from ninja.security import HttpBearer

from allauth.account.adapter import get_adapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from allauth.socialaccount.helpers import complete_social_login
from allauth.account.models import EmailAddress as allauthEmailAddress
from allauth.account.models import EmailConfirmation as allauthEmailConfirmation
from allauth.account.decorators import verified_email_required
from allauth.account.utils import send_email_confirmation
from allauth.account.signals import email_confirmed, user_signed_up

from .schema import LoginResponseSchema, SignupRequestSchema, AddEmployeeSchema, StaffSignupRequestSchema, SignupResponseSchema, SocialLoginRequestSchema, \
    NotFoundSchema, EmailLoginRequestSchema, EmailVerificationSchema, SuccessMessageSchema, PasswordChangeRequestSchema, PasswordChangeRequestDoneSchema, \
                PasswordResetRequestSchema, PasswordResetRequestDoneSchema, SocialAccountSignupSchema, ResendEmailCodeSchema, StaffSignupRequestSchema, StaffSignupResponseSchema, \
                    AddEmployeeSchema, AcceptInvitation

from core.models import EmailVerification, SmsVerification

''' 
from customers.models import Customer
from orders.models import DeliveryAgent

from inventory.models import SupplyManager
 '''
from restaurants.models import Staff
from django.conf import settings

User = get_user_model()
router = Router()


"""
    GLOBAL VARIABLES
"""
registration_successful = "Registration successful"


#############      SIGNALS EMITTED        ############
### EMITTED ONLY WHEN USER SIGNED UP THROUGH PROVIDERS
"""
SOCIAL ACCOUNTS NOT SETUP YET.
"""
@receiver(user_signed_up)
def socialaccount_user_signup(request, user, **kwargs):
    if request.session.get("actor_type"):
        actor_type = request.session.get('actor_type')
        # Get the actor type from the session that was stored during the signup.
        ''' if actor_type == 'customer':
            user = User.objects.get(email = user.email)
            try:
                 customer = user.customer  # Retrieve existing Customer instance
            except Customer.DoesNotExist:
                 # Create a new Customer instance associated with this User
                customer = Customer(user_ptr=user, username=user.username, email=user.email, address="abuja")
                customer.set_password(user.password)
                customer.save()
            
        elif actor_type == 'supplymanager':
            SupplyManager.objects.create_user(user=user) '''
        ''' if actor_type == 'chef':
            Chef.objects.create_user(user=user) '''
        ''' elif actor_type == 'deliveryagent':
            DeliveryAgent.objects.create_user(user=user) '''
        
        del request.session['actor_type']



### MANUAL SIGNUPS WITH EMAIL AND OTHER CREDENTIALS  ###
@router.post("/owner-signup", tags = ["Default Signup"])
def owner_signup(request, data: SignupRequestSchema):
    # Model signup
    if data.actor_type != "owner":
        return JsonResponse({"message": "Not a restaurant owner."})
    
    owner = User.objects.create(first_name = data.first_name, last_name = data.last_name, email = data.email, phone_number = data.phone_number, username = data.username)
    owner.set_password(data.password)
    owner.is_active = False
    owner.save()
    
    # Get the model instance for allauth implementation.
    allauthemail_address, _ = allauthEmailAddress.objects.get_or_create(
        user=owner,
        email=data.email,
        defaults={'verified': False, 'primary': True}
    )

    # Create EmailConfirmation instance and send verification mail
    confirmation = allauthEmailConfirmation.create(email_address = allauthemail_address)
    confirmation.send(request = request, signup=True)
    confirmation.sent = timezone.now()
    confirmation.save()
    
    # Return info.
    return {"message": registration_successful}


@router.post("/add-employee")
def add_employee(request, data: AddEmployeeSchema):
    if data.actor_type != "owner":
        return JsonResponse({"message": "Not a restaurant owner, only restaurant owners can add employee."})
    
    # Get restaurant availability
    
    try:
        restaurant = Restaurant.objects.get(owner=request.user)
        
    except Restaurant.DoesNotExist:
        return JsonResponse({"message": "Restaurant does not exist"})
    
    staff = Staff.objects.create(email = data.email, role = data.role, restaurants = restaurant)
    staff.is_active = False
    staff.save()
    
    # Get the model instance for allauth implementation.
    allauthemail_address, _ = allauthEmailAddress.objects.get_or_create(
        user=staff,
        email=data.email,
        defaults={'verified': False, 'primary': True}
    )

    # Create EmailConfirmation instance and send verification mail
    confirmation = allauthEmailConfirmation.create(email_address = allauthemail_address)
    confirmation.send(request = request, signup=True)
    confirmation.sent = timezone.now()
    confirmation.save()
    
    # Return info.
    return {"message": registration_successful}



@router.post("/accept-invite")
def staff_signup(request, data:StaffSignupRequestSchema):
    
    # Get restaurant availability
    ''' 
    try:
        restaurant = Restaurant.objects.get(name=data.works_at)
        
    except Restaurant.DoesNotExist:
        return JsonResponse({"message": "Restaurant does not exist"})
     '''
    
    # Model signup
    try:
        staff = Staff.objects.get(email = data.email)
    except Staff.DoesNotExist:
        return JsonResponse({"message": "Staff doesn't exist!"})
    
    staff_update = staff.objects.update(first_name = data.first_name, last_name = data.last_name, phone_number = data.phone_number, username = data.username, role = data.role)
    staff_update.set_password(data.password)
    staff_update.is_active = False
    staff_update.save()
    
    # Get the model instance for allauth implementation.
    allauthemail_address, _ = allauthEmailAddress.objects.get_or_create(
        user=staff_update,
        email=data.email,
        defaults={'verified': True, 'primary': True}
    )
    
    # Return info.
    return {"message": registration_successful}
    


@router.get("confirm-email/{key_token}", url_name="verifybytoken")
def verify_key(request, key_token: str):
    
    try:
        # Try to use the key as-is first
        email_confirmation = allauthEmailConfirmation.objects.get(key=key_token)
    except allauthEmailConfirmation.DoesNotExist:
        try:
            # If that fails, try decoding it
            decoded_key = urlsafe_base64_decode(key_token).decode()
            email_confirmation = allauthEmailConfirmation.objects.get(key=decoded_key)
        except (TypeError, ValueError, OverflowError, allauthEmailConfirmation.DoesNotExist):
            print("Failed to find EmailConfirmation with provided key")
            return {"message": "Invalid or expired token"}
    
    try:
        # Confirm the email here with all-auth
        email_confirmation.confirm(request)
        user = User.objects.get(email = email_confirmation.email_address)
        
        user.is_active = True
        user.save()
        
        # Delete the email confirmation instance created
        allauthemail_address = allauthEmailAddress.objects.get(email=user.email)
        allauthEmailConfirmation.objects.get(email_address = allauthemail_address).delete()
        
        return {"message": "Email verified successfully"}
    except Exception as e:
        return {"message": "Error during email verification"}


#### VERIFICATION BASICALLY FOR PEOPLE THAT DID NOT SIGN IN WITH GOOGLE ACCOUNT PROVIDER ####
#Phone Number verification
@router.post("/verify-phonenumber")
def verify_phonenumber(request):
    pass

#### RESEND-EMAIL VERIFICATION CODE ####
@router.post("/resend-emailcode")
def resend_emailcode(request, data: ResendEmailCodeSchema):
    try:
        allauthemail_address = allauthEmailAddress.objects.get(email=data.email)
        allauthEmailConfirmation.objects.get(email_address = allauthemail_address).delete()
        
        confirmation = allauthEmailConfirmation.create(email_address = allauthemail_address)
        confirmation.send(request = request, signup=True)
        confirmation.sent = timezone.now()
        confirmation.save()
        
    except allauthEmailAddress.DoesNotExist:
        return JsonResponse({"message": "User does not exist in the database"})
           