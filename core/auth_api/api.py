
import secrets
from random import randint

import jwt
from datetime import timedelta as datetime_timedelta
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
from rest_framework_simplejwt.tokens import RefreshToken

from core.auth_api.schema import CustomerSignupRequestSchema
from core.auth_api.token_management import AuthBearer
from core.CustomFiles.CustomBackend import EmailAuthBackend, PhoneAuthBackend
from core.models import EmailVerification
from customers.models import Customer
from inventory.models import SupplyManager
from orders.models import DeliveryAgent
from restaurants.models import Restaurant, Staff
from inventory.models import Supplier

from .schema import (
    AcceptInvitation,
    AddEmployeeSchema,
    DeliveryAgentSignupRequestSchema,
    EmailLoginRequestSchema,
    EmailVerificationSchema,
    JWTLoginResponseSchema,
    LoginResponseSchema,
    LogoutResponseSchema,
    NotFoundSchema,
    PasswordChangeRequestDoneSchema,
    PasswordChangeRequestSchema,
    PasswordResetRequestDoneSchema,
    PasswordResetRequestSchema,
    PhoneNumberLoginRequestSchema,
    PhoneNumberVerificationRequestSchema,
    ResendEmailCodeSchema,
    SignupRequestSchema,
    SignupResponseSchema,
    SocialAccountSignupSchema,
    SocialLoginRequestSchema,
    StaffSignupRequestSchema,
    StaffSignupResponseSchema,
    SuccessMessageSchema,
)
from .token_management import create_token, CustomRefreshToken, generate_code

User = get_user_model()
router = Router()


"""
    GLOBAL VARIABLES
"""
registration_successful = "Registration successful"

def phoneNumberExist(phone_number):
    try:
        if User.objects.filter(phone_number = phone_number).exists():
            return {"status": True, "message": "User with phone number exists"}
        else:
            return {"status": False, "message": "Phone number is available for you"}
        
    except Exception as e:
        return {"status": False, "message": e}
    
def emailAddressExist(email):
    try:
        if User.objects.filter(email = email).exists():
            return {"status": True, "message": "User with email exists"}
        else:
            return {"status": False, "message": "Email is available for you"}
        
    except Exception as e:
        return {"status": False, "message": e}


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
            else:
                email_instance = EmailVerification.objects.get(user = instance)
                email_instance.email_code = generate_code(6)
                email_instance.expires_at=django_timezone.now() + django_timezone.timedelta(minutes = 10)
                email_instance.save()
                
            email_token = EmailVerification.objects.filter(user = instance).last()
            subject =  "Email Verification"
            message = f"""
                    Hello, here is your one time email verification code {email_token.email_code}
                    """
            business_email_sender ="dev@kittchens.com"
            receiver = [instance.email]
            try:
                email_send = send_mail(subject, message, business_email_sender, receiver)
            except Exception:
                email_send = False
            
            if email_send:
                return {"message": "email sent", "status_code": 200}
                
            else:
                
                return {"message": "email not sent", "status_code": 404}


### EMITTED ONLY WHEN USER SIGNED UP THROUGH PROVIDERS
"""
SOCIAL ACCOUNTS NOT SETUP YET.
"""



@receiver(user_signed_up)
def socialaccount_user_signup(request, user, **kwargs):
    print("\n"*5,request.session, "\n"*5)
    if request.session.get("actor_type"):
        print("Session is here", request.session.get("actor_type"))
        ''' actor_type = request.session.get("actor_type")  # noqa: F841
        # Get the actor type from the session that was stored during the signup.
        if actor_type == 'customer':
            user = User.objects.get(email = user.email)
            
            if not isinstance(user, Customer) or not user.customer: 
                # Retrieve existing Customer instance
            
                 # Create a new Customer instance associated with this User
                customer = Customer(user_ptr=user, address="abuja")
                customer.set_password(user.password)
                customer.is_active = True
                user.save() '''
                #user.delete()
                #customer.save()
            
        ''' elif actor_type == 'supplymanager':
            SupplyManager.objects.create_user(user=user) '''
        """ if actor_type == 'chef':
            Chef.objects.create_user(user=user) ""
        "" elif actor_type == 'deliveryagent':
            DeliveryAgent.objects.create_user(user=user) """

        del request.session["actor_type"]
        
    else:
        print("Session is not here")


### MANUAL SIGNUPS WITH EMAIL AND OTHER CREDENTIALS  ###

# Both restaurant owners and supplier owners signup endpoint/function.
@router.post("/owner-signup", tags=["Default Signup"], auth=None, response={200: SuccessMessageSchema, 403: NotFoundSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def owner_signup(request, data: SignupRequestSchema):
    # Model signup
    if data.actor_type != "owner":
        return JsonResponse({"message": "Not a business owner."})
    
    phone_number_exist = phoneNumberExist(data.phone_number)
    if phone_number_exist["status"] == True:
        return 404, {"message": "User with this phone number already exists"}
    
    email_exist = emailAddressExist(data.email)
    if email_exist["status"] == True:
        return 404, {"message": "User with this email address already exists"}
    
    try:
        if not (User.objects.filter(email = data.email).exists()):
            owner = User.objects.create(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                phone_number=data.phone_number,
            )
            owner.set_password(data.password)
            owner.is_active = False
            owner_grp, _ = Group.objects.get_or_create(name="Supplier Owner")
            owner.groups.add(owner_grp)
            owner.save()
        else:
            return 404, {"message": "User already exists"}
        
        if (data.is_mobile == True):
            owner = User.objects.get(email = data.email)
            EmailVerification.objects.create(user = owner, expires_at=django_timezone.now() + django_timezone.timedelta(minutes = 10))
            
            #email_token = EmailVerification.objects.filter(user = owner).last()
            try:
                allauthemail_address, _ = allauthEmailAddress.objects.get_or_create(
                user=owner,
                email=data.email,
                defaults={"verified": False, "primary": True},
            )
                email_send_func = create_email_token(sender = None, instance = owner, created = True)
                if email_send_func["status_code"] == 200:
                    return 200, {"message": "Email verification code has been sent"}
                else:
                    return 404, {"message": "Email not sent"}
                
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
            return 200, {"message": registration_successful}

    except Exception as e:
        return 500, {"message": e}

''' 

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

 '''

@router.post("/add-employee", tags=["Accept and Invite"], response={200: SuccessMessageSchema, 403: NotFoundSchema, 404: NotFoundSchema})
def add_employee(request, data: AddEmployeeSchema):
    if data.actor_type != "owner":
        return 403, {"message": "Not a restaurant owner, only restaurant owners can add employee."}
        

    # Get restaurant availability
    try:
        restaurant = Restaurant.objects.get(owner=request.user)

    except Restaurant.DoesNotExist:
        return 404, {"message": "Restaurant does not exist"}

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
    return 200, {"message": registration_successful}


@router.post("/accept-invite", response={200: SuccessMessageSchema, 403: NotFoundSchema, 404: NotFoundSchema})
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
        return 404, {"message": "Staff doesn't exist!"}

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
    return 200, {"message": registration_successful}


@router.post("/customer-signup", tags=["Default Signup"], response={200: SuccessMessageSchema, 404: NotFoundSchema})
def customer_signup(request, data: CustomerSignupRequestSchema):
    if data.actor_type != "customer":
        return 404, {"message": "Not a customer."}
    
    phone_number_exist = phoneNumberExist(data.phone_number)
    if phone_number_exist["status"] == True:
        return 404, {"message": "User with this phone number already exists"}
    
    email_exist = emailAddressExist(data.email)
    if email_exist["status"] == True:
        return 404, {"message": "User with this email address already exists"}

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
        defaults={"verified": False, "primary": True},
    )
    return 200, {"message": f"Customer {data.email} has been saved"}


@router.post("/deliveryagent-signup", tags=["Default Signup"], response={200: SuccessMessageSchema, 403: NotFoundSchema, 404: NotFoundSchema})
def deliveryagent_signup(request, data: DeliveryAgentSignupRequestSchema):
    if data.actor_type != "deliveryagent":
        return 403, {"message": "Not a deliveryagent."}
    
    try:
        country = Country.objects.get(name=data.address)
    except Country.DoesNotExist:
        return 404, {"message": "Country not accepted for now"}
    
    phone_number_exist = phoneNumberExist(data.phone_number)
    if phone_number_exist["status"] == True:
        return 404, {"message": "User with this phone number already exists"}
    
    email_exist = emailAddressExist(data.email)
    if email_exist["status"] == True:
        return 404, {"message": "User with this email address already exists"}

    deliveryagent = DeliveryAgent.objects.create(
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
            email=data.email,
            address=country,
            terms_and_condition=data.terms_and_condition,
    )
    deliveryagent.set_password(data.password)
    deliveryagent.is_active = False
    deliveryagent.save()
    return 200, {"message": "Delivery agent account registered, check your email for verification"}


@router.get("confirm-email/{key_token}", url_name="verifybytoken", auth=None, response={200: SuccessMessageSchema, 403: NotFoundSchema, 404: NotFoundSchema})
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
            return 403, {"message": "Invalid or expired token"}
    
    try:
        # Confirm the email here with all-auth
        email_confirmation.confirm(request)
        user = User.objects.get(email = email_confirmation.email_address)
        
        user.is_active = True
        user.save()
        login(request, user, backend="EmailAuthBackend")
        # Delete the email confirmation instance created
        allauthemail_address = allauthEmailAddress.objects.get(email=user.email)
        allauthEmailConfirmation.objects.get(email_address = allauthemail_address).delete()
        
        return 200, {"message": "Email verified successfully"}
    except Exception as e:
        return 404, {"message": "Error during email verification"}


#### VERIFICATION BASICALLY FOR PEOPLE THAT DID NOT SIGN IN WITH GOOGLE ACCOUNT PROVIDER ####
# Email verification

@router.post("/verify-email", response = {200: JWTLoginResponseSchema, 404: NotFoundSchema}, tags=["Email Verification"])
def verify_email(request, data: EmailVerificationSchema):
    email = data.email
    email_token = data.token
    user = User.objects.get(email = email)
    verify_model = EmailVerification.objects.get(user = user)#.last()
    if verify_model.expires_at > django_timezone.now():
        if verify_model.email_code == email_token:
            allauthuser = allauthEmailAddress.objects.get_or_create(user = user, email = data.email, defaults={"verified": True, "primary": True})
            #allauthuser.save()
            user.is_active = True
            user.save()
            login(request, user, backend="EmailAuthBackend")
             # Delete the email verification instance created
            EmailVerification.objects.get(user = user).delete()
            
            token_expiry_period, access_token_period = 7, 120
            token = CustomRefreshToken.for_user(str(user))
            token.set_exp(lifetime=datetime_timedelta(days=token_expiry_period))
            access_token = token.access_token
            access_token.set_exp(lifetime=datetime_timedelta(minutes=access_token_period))
            
            user.last_login = django_timezone.now()
            user.save(update_fields=['last_login'])
            
            return 200, {
                "refresh": str(token),
                "access": str(access_token),
                "user_id": str(user),
                "actor_type": str(getActorType(user.email))
            }
        else:
            return 404, {"message": "Invalid verification code"}
    else:
        return 404, {"message": "User has exceeded token validity period of 10 minutes"}


# Phone Number verification
@router.post("/verify-phonenumber")
def verify_phonenumber(request):
    pass


@router.post("/check-phonenumber", response={200: SuccessMessageSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def check_phonenumber(request, data: PhoneNumberVerificationRequestSchema):
    try:
        phone_number_exist = phoneNumberExist(data.phone_number)
        if phone_number_exist["status"] == False:
            return 200, {"message": "Phone number is available for use"}
        else:
            return 404, {"message": "User with this phone number already exists"}
        
    except Exception as e:
        return 500, {"message": f"{e}"}

@router.post("/verify-password", auth=AuthBearer(), response={200: SuccessMessageSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def verify_password(request, data: LoginResponseSchema):
    try:
        user_id = request.auth["user_id"]
        user = User.objects.get(id = user_id)
        user.check_password(data.token)
        return 200, {"message": "Password verified."}
        
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
        
    
#### RESEND-EMAIL VERIFICATION CODE ####

@router.post("/resend-emailcode", auth=None, response={200: SuccessMessageSchema, 403: NotFoundSchema, 404: NotFoundSchema})
def resend_emailcode(request, data: ResendEmailCodeSchema):
    try:
        if data.is_mobile == True:
            try:
                user = User.objects.get(email = data.email)
            except User.DoesNotExist:
                return 404, {"message": "User does not exist"}
            email_send_func = create_email_token(sender = None, instance = user, created = True)
            if email_send_func["status_code"] == 200:
                return 200, {"message": "Email verification code has been sent"}
            else:
                return 404, {"message": "Email not sent"}
            
        else:
            try:
                allauthemail_address = allauthEmailAddress.objects.get(email=data.email)
            except Exception as e:
                return 404, {"message": "Error fetching user"}
            allauthEmailConfirmation.objects.get(
                email_address=allauthemail_address
            ).delete()

            confirmation = allauthEmailConfirmation.create(
                email_address=allauthemail_address
            )
            confirmation.send(request=request, signup=True)
            confirmation.sent = django_timezone.now()
            confirmation.save()
            return 200, {"message": "Email verification resent"}

    except allauthEmailAddress.DoesNotExist:
        return 404, {"message": "User does not exist in the database"}


@login_required
@router.post("/logout", auth=AuthBearer(), response={200: SuccessMessageSchema, 403: NotFoundSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def logout(request, data: LogoutResponseSchema):
    print("Printing from api.py",request.auth)
    try:
        token = CustomRefreshToken(data.refresh_token)
        if request.auth["email"] == token["email"]:
            user = User.objects.get(id = token["user_id"])
            if user.is_authenticated:
                token.blacklist()
                django_logout(request)
                return 200, {"message": "User has been logged out."}
            else:
                return 404, {"message": "User need to be logged in before performing this action"}
        return 403, {"message": "Error in user's details"}
    except Exception as e:
        return 404, {"message": "Invalid Token"}
            
   

def getActorType(email):
    User = get_user_model()
    try:
        user = User.objects.get(email = email)
        if isinstance(user, Customer):
            return "customer"
        elif isinstance(user, DeliveryAgent):
            return 'deliveryagent'
        elif isinstance(user, Staff):
            return "staff"
        elif isinstance(user, SupplyManager):
            return "supplymanager"
        elif Supplier.objects.filter(owner = user).exists():
            return "supplyowner"
        elif Restaurant.objects.filter(owner = user).exists():
            return "restaurantowner"
        else:
            return "unknown_actortype"
        
    except User.DoesNotExist:
        return None


#### SIGN IN ENDPOINTS ##########
# Sign in with email
@router.post(
    "/mobile-email-signin",
    auth=None,
    tags=["Manual SignIn"],
    response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema},
)
def email_login(request, data: EmailLoginRequestSchema):
    email = data.email
    password = data.password
    remember_me = data.remember_me

    if not email or not password:
        return 404, "Incomplete details"

    try:
        User.objects.get(email = email)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token_expiry_period = 14 if remember_me is True else 1
            access_token_period = 60 if remember_me is True else 5
            login(request, user, backend="EmailAuthBackend")
            
            token = CustomRefreshToken.for_user(str(user))
            token.set_exp(lifetime=datetime_timedelta(days=token_expiry_period))
            access_token = token.access_token
            access_token.set_exp(lifetime=datetime_timedelta(minutes=access_token_period))
            
            user.last_login = django_timezone.now()
            user.save(update_fields=['last_login'])
            
            ''' token = create_token( 
                user_id=str(user.id), expiry_period=token_expiry_period
            ) '''
            
            
            return 200, {
                "refresh": str(token),
                "access": str(access_token),
                "user_id": str(user),
                "actor_type": str(getActorType(user.email))
            }
        else:
            return 404, {"message": "User does not exist"}

    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}

    except Exception as e:
        print("\n"*5,e,"\n"*5)
        return 404, {"message": str(e)}


# Sign in with phone_number
@router.post(
    "/mobile-phone-signin",
    auth=None,
    tags=["Manual SignIn"],
    response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema},
)
def phone_number_login(request, data: PhoneNumberLoginRequestSchema):
    phone_number = data.phone_number
    password = data.password
    remember_me = data.remember_me

    if not phone_number or not password:
        return 404, "Incomplete details"

    try:
        User.objects.get(phone_number = phone_number)
        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            token_expiry_period = 14 if remember_me is True else 1
            access_token_period = 60 if remember_me is True else 5
            login(request, user, backend="PhoneAuthBackend")
            
            token = CustomRefreshToken.for_user(str(user))
            token.set_exp(lifetime=datetime_timedelta(days=token_expiry_period))
            access_token = token.access_token
            access_token.set_exp(lifetime=datetime_timedelta(minutes=access_token_period))
            
            user.last_login = django_timezone.now()
            user.save(update_fields=['last_login'])
            
            ''' token = create_token( 
                user_id=str(user.id), expiry_period=token_expiry_period
            ) '''
            
            
            return 200, {
                "refresh": str(token),
                "access": str(access_token),
                "user_id": str(user),
                "actor_type": str(getActorType(user.email))
            }
        else:
            return 404, {"message": "User does not exist"}

    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}

    except Exception as e:
        print("\n"*5,e,"\n"*5)
        return 404, {"message": str(e)}


@router.get("/google/{actor_type}", tags=["Social Auth"], auth=None, response={200: SuccessMessageSchema, 403: NotFoundSchema, 404: NotFoundSchema})
def google_auth(request: HttpRequest, actor_type:str):
    try:
        request.session["actor_type"] = actor_type
        callback_url = request.build_absolute_uri(reverse('google_callback'))
        adapter = GoogleOAuth2Adapter(request)
        return redirect("/accounts/google/login/")
    
    except Exception:
        return 403, {"error": "actor_type required"}
