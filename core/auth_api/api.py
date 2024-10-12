
import secrets
from random import randint

import jwt
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.decorators import verified_email_required
from allauth.account.models import EmailAddress as allauthEmailAddress
from allauth.account.models import EmailConfirmation as allauthEmailConfirmation
from allauth.account.signals import email_confirmed, user_signed_up
from allauth.account.utils import complete_signup, send_email_confirmation
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from cities_light.models import Country
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone as django_timezone
from django.utils.http import urlsafe_base64_decode
from ninja import Router
from ninja.security import HttpBearer

from core.auth_api.schema import CustomerSignupRequestSchema
from core.CustomFiles.CustomBackend import EmailAuthBackend, PhoneAuthBackend
from core.models import EmailVerification
from customers.models import Customer
from inventory.models import SupplyManager
from orders.models import DeliveryAgent
from restaurants.models import Restaurant, Staff

from .schema import (
    AcceptInvitation,
    AddEmployeeSchema,
    DeliveryAgentSignupRequestSchema,
    EmailLoginRequestSchema,
    EmailVerificationSchema,
    LoginResponseSchema,
    NotFoundSchema,
    PasswordChangeRequestDoneSchema,
    PasswordChangeRequestSchema,
    PasswordResetRequestDoneSchema,
    PasswordResetRequestSchema,
    PhoneNumberLoginRequestSchema,
    ResendEmailCodeSchema,
    SignupRequestSchema,
    SignupResponseSchema,
    SocialAccountSignupSchema,
    SocialLoginRequestSchema,
    StaffSignupRequestSchema,
    StaffSignupResponseSchema,
    SuccessMessageSchema,
)
from .token_management import *  # noqa: F403

User = get_user_model()
router = Router()


"""
    GLOBAL VARIABLES
"""
registration_successful = "Registration successful"


#############      SIGNALS EMITTED        ############
@receiver(post_save, sender = Customer)
@receiver(post_save, sender = SupplyManager)
@receiver(post_save, sender = DeliveryAgent)
def create_email_token(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser: 
            if not EmailVerification.objects.filter(user=instance).exists(): 
                EmailVerification.objects.create(user = instance, expires_at=django_timezone.now() + django_timezone.timedelta(minutes = 10))
                instance.is_active = False
                instance.save()
            email_token = EmailVerification.objects.filter(user = instance).last()
            subject =  "Email Verification"
            message = f"""
                    Hello, here is your one time email verification code {email_token.email_code}
                    """
            business_email_sender ="dev@kittchens.com"
            receiver = [instance.email]
            email_send = send_mail(subject, message, business_email_sender, receiver)
            
            if email_send:
                return JsonResponse({"message": "email sent", "status_code": 200})
                
            else:
                
                return JsonResponse({"message": "email not sent", "status_code": 404})


### EMITTED ONLY WHEN USER SIGNED UP THROUGH PROVIDERS
"""
SOCIAL ACCOUNTS NOT SETUP YET.
"""



@receiver(user_signed_up)
def socialaccount_user_signup(request, user, **kwargs):
    print("\n"*5,request.session, "\n"*5)
    if request.session.get("actor_type"):
        print("Session is here", request.session.get("actor_type"))
        actor_type = request.session.get("actor_type")  # noqa: F841
        # Get the actor type from the session that was stored during the signup.
        if actor_type == 'customer':
            user = User.objects.get(email = user.email)
            
            if not isinstance(user, Customer): 
                # Retrieve existing Customer instance
            
                 # Create a new Customer instance associated with this User
                customer = Customer(user_ptr=user, address="abuja")
                customer.set_password(user.password)
                user.delete()
                customer.save()
            
        elif actor_type == 'supplymanager':
            SupplyManager.objects.create_user(user=user)
        """ if actor_type == 'chef':
            Chef.objects.create_user(user=user) ""
        "" elif actor_type == 'deliveryagent':
            DeliveryAgent.objects.create_user(user=user) """

        del request.session["actor_type"]
        
    else:
        print("Session is not here")


### MANUAL SIGNUPS WITH EMAIL AND OTHER CREDENTIALS  ###


@router.post("/owner-signup", tags=["Default Signup"], auth=None)
def owner_signup(request, data: SignupRequestSchema):
    # Model signup
    if data.actor_type != "owner":
        return JsonResponse({"message": "Not a business owner."})
    
    try:
        if not (User.objects.filter(email = data.email).exists()):
            owner = User.objects.create(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                phone_number=data.phone_number,
                username=data.username,
            )
            owner.set_password(data.password)
            owner.is_active = False
            owner.save()
        else:
            return {"message": "User already exists"}
        
        if (data.is_mobile == True):
            owner = User.objects.get(email = data.email)
            #EmailVerification.objects.create(user = owner, expires_at=django_timezone.now() + django_timezone.timedelta(minutes = 10))
            
            #email_token = EmailVerification.objects.filter(user = owner).last()
            try:
                email_send_func = create_email_token(sender = None, instance = owner, created = True)
                return email_send_func
                
            except Exception as e:
                print(e)
                return {"message": "error sending email"}
            
            ''' 
            subject =  "Email Verification"
            message = f"""
                    Hello, here is your one time email verification code {email_token.email_code}
                    """
            sender ="dev@kittchens.com"
            receiver = [owner.email]
            
            email_send = send_mail(subject, message, sender, receiver)
            
            if email_send:
                return JsonResponse({"message": "email sent"})
                #return 200, EmailVerificationSchema(email = data.email)
            else:
                #return 404, NotFoundSchema(message = "Not verified")
                
                return JsonResponse({"message": "email not sent"}) '''
        
        else:
            # Get the model instance for allauth implementation.
            owner = User.objects.get(email = data.email)
            allauthemail_address, _ = allauthEmailAddress.objects.get_or_create(
                user=owner, email=data.email, defaults={"verified": False, "primary": True}
            )

            # Create EmailConfirmation instance and send verification mail
            confirmation = allauthEmailConfirmation.create(email_address=allauthemail_address)
            confirmation.send(request=request, signup=True)
            confirmation.sent = django_timezone.now()
            confirmation.save()

            # Return info.
            return {"message": registration_successful}

    except Exception as e:
        return {"message": e}



@router.post("/supply-owner-signup", tags = ["Default Signup"])
def supply_owner_signup(request, data: SignupRequestSchema):
    # Model signup
    if data.actor_type != "owner":
        return JsonResponse({"message": "Not an owner."})
    
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
    confirmation.sent = django_timezone.now()
    confirmation.save()
    
    # Return info.
    return {"message": registration_successful}



@router.post("/add-employee", tags=["Accept and Invite"])
def add_employee(request, data: AddEmployeeSchema):
    if data.actor_type != "owner":
        return JsonResponse(
            {
                "message": "Not a restaurant owner, only restaurant owners can add employee."
            }
        )

    # Get restaurant availability
    try:
        restaurant = Restaurant.objects.get(owner=request.user)

    except Restaurant.DoesNotExist:
        return JsonResponse({"message": "Restaurant does not exist"})

    staff = Staff.objects.create(
        email=data.email, role=data.role, restaurants=restaurant
    )
    staff.is_active = False
    staff.save()

    # Get the model instance for allauth implementation.
    allauthemail_address, _ = allauthEmailAddress.objects.get_or_create(
        user=staff, email=data.email, defaults={"verified": False, "primary": True}
    )

    # Create EmailConfirmation instance and send verification mail
    confirmation = allauthEmailConfirmation.create(email_address=allauthemail_address)
    confirmation.send(request=request, signup=True)
    confirmation.sent = django_timezone.now()
    confirmation.save()

    # Return info.
    return {"message": registration_successful}


@router.post("/accept-invite")
def staff_signup(request, data: StaffSignupRequestSchema):
    # Get restaurant availability
    """
    try:
        restaurant = Restaurant.objects.get(name=data.works_at)

    except Restaurant.DoesNotExist:
        return JsonResponse({"message": "Restaurant does not exist"})
    """

    # Model signup
    try:
        staff = Staff.objects.get(email=data.email)
    except Staff.DoesNotExist:
        return JsonResponse({"message": "Staff doesn't exist!"})

    staff_update = staff.objects.update(
        first_name=data.first_name,
        last_name=data.last_name,
        phone_number=data.phone_number,
        username=data.username,
        role=data.role,
    )
    staff_update.set_password(data.password)
    staff_update.is_active = False
    staff_update.save()

    # Get the model instance for allauth implementation.
    allauthemail_address, _ = allauthEmailAddress.objects.get_or_create(
        user=staff_update,
        email=data.email,
        defaults={"verified": True, "primary": True},
    )

    # Return info.
    return {"message": registration_successful}


@router.post("/customer-signup", tags=["Default Signup"])
def customer_signup(request, data: CustomerSignupRequestSchema):
    if data.actor_type != "customer":
        return JsonResponse({"message": "Not a customer."})

    customer = Customer.objects.create(
        first_name=data.first_name,
        last_name=data.last_name,
        phone_number=data.phone_number,
        email=data.email,
    )
    customer.set_password(data.password)
    customer.is_active = False
    customer.save()
    
    allauthemail_address, _ = allauthEmailAddress.objects.get_or_create(
        user=customer,
        email=data.email,
        defaults={"verified": True, "primary": True},
    )
    return JsonResponse({"message": "Saved"})


@router.post("/deliveryagent-signup", tags=["Default Signup"])
def deliveryagent_signup(request, data: DeliveryAgentSignupRequestSchema):
    if data.actor_type != "deliveryagent":
        return JsonResponse({"message": "Not a deliveryagent."})
    try:
        country = Country.objects.get(name=data.address)
    except Country.DoesNotExist:
        return JsonResponse({"message": "Country does not exist"})

    deliveryagent = DeliveryAgent.objects.create(
        first_name=data.first_name,
        last_name=data.last_name,
        phone_number=data.phone_number,
        email=data.email,
        address=country,
    )
    deliveryagent.set_password(data.password)
    deliveryagent.is_active = False
    deliveryagent.save()
    return JsonResponse({"message": "Saved"})


@router.get("confirm-email/{key_token}", url_name="verifybytoken", auth=None)
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
# Email verification

@router.post("/verify-email")#, response = {404: NotFoundSchema}, tags=["Email Verification"])
def verify_email(request, data: EmailVerificationSchema):
    email = data.email
    email_token = data.token
    user = User.objects.get(email = email)
    verify_model = EmailVerification.objects.get(user = user)#.last()
    if verify_model.email_code == email_token:
        if verify_model.expires_at > django_timezone.now():
            allauthEmailAddress.objects.get_or_create(user = user, email = data.email, defaults={"verified": True, "primary": True})
            user.is_active = True
            user.save()
            
            EmailVerification.objects.get(user = user).delete()
            return JsonResponse({"message": "Email verified"})


# Phone Number verification
@router.post("/verify-phonenumber")
def verify_phonenumber(request):
    pass



#### RESEND-EMAIL VERIFICATION CODE ####

@router.post("/resend-emailcode", auth=None)
def resend_emailcode(request, data: ResendEmailCodeSchema):
    try:
        allauthemail_address = allauthEmailAddress.objects.get(email=data.email)
        allauthEmailConfirmation.objects.get(
            email_address=allauthemail_address
        ).delete()

        confirmation = allauthEmailConfirmation.create(
            email_address=allauthemail_address
        )
        confirmation.send(request=request, signup=True)
        confirmation.sent = django_timezone.now()
        confirmation.save()

    except allauthEmailAddress.DoesNotExist:
        return JsonResponse({"message": "User does not exist in the database"})


@login_required
@router.post("/logout")
def logout(request):
    print(request.auth)
    try:
        if request.auth is not None:
            user = User.objects.get(id=str(request.auth))
            django_logout(request, user)
            return JsonResponse({"message": "User has been logged out."})
        else:
            return JsonResponse({"message": "User has been logged out."})

    except User.DoesNotExist:
        return JsonResponse({"message": "User does not exist in our database"})

    except Exception as e:
        return JsonResponse(
            {"message": f"An error occurred while processing your exist.\n{e}\n"}
        )


#### SIGN IN ENDPOINTS ##########
# Sign in with email
@router.post(
    "/email-signin",
    auth=None,
    tags=["Manual SignIn"],
    response={200: LoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema},
)
def email_login(request, data: EmailLoginRequestSchema):
    email = data.email
    password = data.password
    remember_me = data.remember_me

    if not email or not password:
        return 404, "Incomplete details"

    try:
        user = authenticate(request, username=email, password=password)
        print(email)
        print(user)
        print(password)
        if user is not None:
            token_expiry_period = 14 if remember_me is True else 1
            login(request, user, backend="EmailAuthBackend")
            token = create_token( 
                user_id=str(user.id), expiry_period=token_expiry_period
            )

            return 200, {"token": token}
        else:
            return 404, {"message": "Not saved, User is none"}

    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}

    except Exception:
        return 404, {"message": "Error in processing requests."}


# Sign in with phone_number
@router.post(
    "/phonenumber-signin",
    auth=None,
    tags=["Manual SignIn"],
    response={200: LoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema},
)
def phonenumber_login(request, data: PhoneNumberLoginRequestSchema):
    phone_number = data.phone_number
    password = data.password
    remember_me = data.remember_me

    if not phone_number or not password:
        return 404, "Incomplete details"

    try:
        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            token_expiry_period = 14 if remember_me is True else 1
            login(request, user, backend="PhoneAuthBackend")
            token = create_token(  # noqa: F405
                user_id=str(user.id), expiry_period=token_expiry_period
            )

            return 200, {"token": token}
        else:
            return 404, {"message": "Not saved, User is not none"}

    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}

    except Exception:
        return 404, {"message": "Error in processing requests."}


@router.get("/google/{actor_type}", tags=["Social Auth"], auth=None)
def google_auth(request: HttpRequest, actor_type:str):
    try:
        request.session["actor_type"] = actor_type
        callback_url = request.build_absolute_uri(reverse('google_callback'))
        adapter = GoogleOAuth2Adapter(request)
        return redirect("/accounts/google/login/")
    
    except Exception:
        return JsonResponse({"error": "actor_type required"})
