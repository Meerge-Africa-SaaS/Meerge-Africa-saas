from random import randint
import secrets
from django.utils import timezone

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

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from allauth.socialaccount.helpers import complete_social_login
from allauth.account.models import EmailAddress as allauthEmailAddress
from allauth.account.decorators import verified_email_required
from allauth.account.utils import send_email_confirmation
from allauth.account.signals import email_confirmed, user_signed_up

from .schema import LoginResponseSchema, SignupRequestSchema, SignupResponseSchema, SocialLoginRequestSchema, \
    NotFoundSchema, EmailLoginRequestSchema, EmailVerificationSchema, SuccessMessageSchema, PasswordChangeRequestSchema, PasswordChangeRequestDoneSchema, \
                PasswordResetRequestSchema, PasswordResetRequestDoneSchema, SocialAccountSignupSchema, ResendEmailCodeSchema, StaffSignupRequestSchema, StaffSignupResponseSchema, \
                    AddEmployeeSchema, AcceptInvitation

from core.models import EmailVerification, SmsVerification

from customers.models import Customer
from orders.models import DeliveryAgent
from restaurant.models import Chef, Staff
from inventory.models import SupplyManager


from django.conf import settings

User = get_user_model()
router = Router()


#############      SIGNALS EMITTED        ############
### EMITTED ONLY WHEN USER SIGNED UP THROUGH PROVIDERS
@receiver(user_signed_up)
def socialaccount_user_signup(request, user, **kwargs):
    if request.session.get("actor_type"):
        actor_type = request.session.get('actor_type')
        # Get the actor type from the session that was stored during the signup.
        if actor_type == 'customer':
            user = User.objects.get(email = user.email)
            try:
                 customer = user.customer  # Retrieve existing Customer instance
            except Customer.DoesNotExist:
                 # Create a new Customer instance associated with this User
                customer = Customer(user_ptr=user, username=user.username, email=user.email, address="abuja")
                customer.set_password(user.password)
                customer.save()
            
        elif actor_type == 'supplymanager':
            SupplyManager.objects.create_user(user=user)
        elif actor_type == 'chef':
            Chef.objects.create_user(user=user)
        elif actor_type == 'deliveryagent':
            DeliveryAgent.objects.create_user(user=user)
        
        del request.session['actor_type']

#### EMITTED WHEN USER SIGNED UP MANUALLY. SIGNAL HERE IS MAINLY FOR EMAIL VERIFICATION FOR MANUALLY SIGNED UP ACTORS
@receiver(post_save, sender = Customer)
@receiver(post_save, sender = SupplyManager)
@receiver(post_save, sender = DeliveryAgent)
@receiver(post_save, sender = Chef)
def create_email_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:            
            EmailVerification.objects.create(user = instance, expires_at=timezone.now() + timezone.timedelta(minutes = 10))
            instance.is_active = False
            instance.save()
            
        email_token = EmailVerification.objects.filter(user = instance).last()
        subject =  "Email Verification"
        message = f"""
                Hello, here is your one time email verification code {email_token.email_code}
                """
        sender ="merge@africa.com"
        receiver = [instance.email]
        
        email_send = send_mail(subject, message, sender, receiver)
        
        if email_send:
            return JsonResponse({"message": "email sent"})
            #return 200, EmailVerificationSchema(email = data.email)
        else:
            #return 404, NotFoundSchema(message = "Not verified")
            return JsonResponse({"message": "email not sent"})

####  EMITTED WHEN RESTAURANT OWNER CREATE AN ACCOUNT FOR A STAFF AND SENDS AN INVITE
@receiver(post_save, sender = Staff)
def send_staff_invite_link(sender, instance, created, **kwargs):
    if created:
        link = "Should generate link here dynamically"
    
        subject =  f"{restaurant_name} invited you"
        message = f"""
                Hello, you received an invitation from {restaurant_name} to join as a {role}. \n
                Click the link below to accept the invitation and complete your profile on the platform.
                
                """
        sender ="merge@africa.com"
        receiver = [instance.email]
        
        email_send = send_mail(subject, message, sender, receiver)
        
        if email_send:
            return JsonResponse({"message": "email sent to the employee"})
            #return 200, EmailVerificationSchema(email = data.email)
        else:
            #return 404, NotFoundSchema(message = "Not verified")
            return JsonResponse({"message": "email not sent to the employee"})
        

#### VERIFICATION BASICALLY FOR PEOPLE THAT DID NOT SIGNED IN WITH SOCIAL ACCOUNT ####
#Phone Number verification
@router.post("/verify-phonenumber")
def verify_phonenumber(request,):
    pass

#Email verification
@router.post("/verify-email")#, response = {404: NotFoundSchema}, tags=["Email Verification"])
def verify_email(request, data: EmailVerificationSchema):
    email = data.email
    email_token = data.token
    user = User.objects.get(email = email)
    verify_model = EmailVerification.objects.get(user = user)#.last()
    if verify_model.email_code == email_token:
        if verify_model.expires_at > timezone.now():
            allauthemail = allauthEmailAddress.objects.get(user = user, email = data.email)
            allauthemail.verified = True
            allauthemail.save()
            user.is_active = True
            user.save()
            
            EmailVerification.objects.get(user = user).delete()
            return HttpResponseRedirect("/login/")

#### RESEND-EMAIL VERIFICATION CODE ####
@router.post("/resend-emailcode", response = {200: EmailVerificationSchema, 404: NotFoundSchema}, tags=["Email Verification"])
def send_emailcode(request, dagita: ResendEmailCodeSchema):
    email = data.email
    if User.objects.filter(email = data.email).exists():
        user = User.objects.get(email = data.email)
        verify_email, status = EmailVerification.objects.get_or_create(user = user)
        print(verify_email)
        verify_email.email_code = secrets.token_hex(3)
        print(verify_email.email_code)
        verify_email.expires_at = timezone.now() + timezone.timedelta(minutes = 10)
        verify_email.save()
        
        subject =  "Email Verification"
        message = f"""
                Hello, here is your one time email verification code {verify_email.email_code}
                """
        sender ="merge@africa.com"
        receiver = [user.email]
        
        email_send = send_mail(subject, message, sender, receiver)
    
        if email_send:
            return 200, EmailVerificationSchema(email = data.email, token = verify_email.email_code)
        else:
            return 404, NotFoundSchema(message = "Not verified")


###############    MANUAL SIGNUPS    ##############

### Customer Signup  ###
@router.post("/customer_signup", response={404: NotFoundSchema}, tags=["Manual Signup"])
def customer_signup(request, data: SignupRequestSchema):
    if User.objects.filter(email = data.email).exists():
        return 404 ,NotFoundSchema(message = "User with this email already exists.")
        ''' elif User.objects.filter(phone_number = data.phone_number).exists():
        return 404 ,NotFoundSchema(message = "User with this phone_number already exists.") '''
    elif User.objects.filter(username = data.username).exists():
        return 404 ,NotFoundSchema(message = "User with this username already exists.")
    
    customer = Customer(username=data.username, email=data.email, address=data.address)
    customer.set_password(data.password)
    customer.save()
    if customer:
        allauthemail = allauthEmailAddress.objects.create(user = customer, email = data.email, primary = True, verified = False)
        return JsonResponse({"message": "email sent"})
    else:
        return 404, NotFoundSchema(message = f"Customer {data.email} not saved")
    
### DeliveryAgent Signup  ###
@router.post("/deliveryagent_signup", response={404: NotFoundSchema}, tags=["Manual Signup"])
def deliveryagent_signup(request, data: SignupRequestSchema):
    if User.objects.filter(email = data.email).exists():
        return 404 ,NotFoundSchema(message = "User with this email already exists.")
        ''' elif User.objects.filter(phone_number = data.phone_number).exists():
        return 404 ,NotFoundSchema(message = "User with this phone_number already exists.") '''
    elif User.objects.filter(username = data.username).exists():
        return 404 ,NotFoundSchema(message = "User with this username already exists.")
    
    deliveryagent = DeliveryAgent(username=data.username, email=data.email) #, address=data.address)
    deliveryagent.set_password(data.password)
    deliveryagent.save()
    
    if deliveryagent:
        allauthemail = allauthEmailAddress.objects.create(user = deliveryagent, email = data.email, primary = True, verified = False)
        return JsonResponse({"message": "email sent"})
    else:
        return 404, NotFoundSchema(message = f"Delivery agents {data.email} not saved")

### Chef Signup  ###
@router.post("/chef_signup", response={200: SignupResponseSchema, 404: NotFoundSchema}, tags=["Manual Signup"])
def chef_signup(request, data: SignupRequestSchema):
    if User.objects.filter(email = data.email).exists():
        return 404 ,NotFoundSchema(message = "User with this email already exists.")
        ''' elif User.objects.filter(phone_number = data.phone_number).exists():
        return 404 ,NotFoundSchema(message = "User with this phone_number already exists.") '''
    elif User.objects.filter(username = data.username).exists():
        return 404 ,NotFoundSchema(message = "User with this username already exists.")
    
    chef = Chef.objects.create(first_name = data.first_name, last_name = data.last_name, phone_number = data.phone_number, username=data.username, email=data.email)#, address=data.address)
    chef.set_password(data.password)
    chef.save()
    if chef:
        allauthemail = allauthEmailAddress.objects.create(user = chef, email = data.email, primary = True, verified = False)
        return JsonResponse({"message": "email sent"})
    else:
        return 404, NotFoundSchema(message = f"Chef {data.email} not saved")
    
### SupplyManager Signup  ###
@router.post("/supplymanager_signup", response={200: SignupResponseSchema, 404: NotFoundSchema}, tags=["Manual Signup"])
def supplymanager_signup(request, data: SignupRequestSchema):
    if User.objects.filter(email = data.email).exists():
        return 404 ,NotFoundSchema(message = "User with this email already exists.")
        ''' elif User.objects.filter(phone_number = data.phone_number).exists():
        return 404 ,NotFoundSchema(message = "User with this phone_number already exists.") '''
    elif User.objects.filter(username = data.username).exists():
        return 404 ,NotFoundSchema(message = "User with this username already exists.")
    
    supplymanager = SupplyManager(username=data.username, email=data.email) #, address=data.address)
    supplymanager.set_password(data.password)
    supplymanager.is_active = False
    supplymanager.save()
    if supplymanager:
        allauthemail = allauthEmailAddress.objects.create(user = supplymanager, email = data.email, primary = True, verified = False)
        return JsonResponse({"message": "email sent"})
    else:
        return 404, NotFoundSchema(message = f"Supplymanager {data.email} not saved")

###  Adding of employee by the Restaurant owner
@router.post("/add-employee", response={200: StaffSignupResponseSchema, 404: NotFoundSchema}, tags=["Manual Signup"])
def staff_signup(request, data: StaffSignupRequestSchema):
    if User.objects.filter(email = data.email).exists():
        return 404 ,NotFoundSchema(message = "User with this email already exists.")
        ''' elif User.objects.filter(phone_number = data.phone_number).exists():
        return 404 ,NotFoundSchema(message = "User with this phone_number already exists.") '''
    elif User.objects.filter(username = data.username).exists():
        return 404 ,NotFoundSchema(message = "User with this username already exists.")
    
    addemployee = Staff.objects.create(username=data.email, email=data.email)#, address=data.address)
    if addemployee:
        allauthemail = allauthEmailAddress.objects.create(user = addemployee, email = data.email, primary = True, verified = False)
        return JsonResponse({"message": "email sent"})
    else:
        return 404, NotFoundSchema(message = f"Supplymanager {data.email} not saved")

## Employee Accept invitation
@router.post("/accept-invitation", response={404: NotFoundSchema}, tags=["Invite-Accept Staff"])
def accept_invitation(request, data: AcceptInvitation):
    email = data.email
    restaurant_name = data.works_at
    password = data.password
    first_name = data.first_name
    last_name = data.last_name
    try:
        new_staff = Staff.objects.get(email = email, works_at = restaurant_name)
        new_staff.first_name = first_name
        new_staff.last_name = last_name
        new_staff.is_active = True
        new_staff.set_password(password)
        new_staff.save()
        new_staff_account = authenticate(request, email = email, password = password)
        if new_staff_account is not None:
            login(request, new_staff_account)
            return render(request, "/dashboard") #will throw error for now, dashboard not existing.
        else:
            return JsonResponse({"message": "We encountered an error while creating your staff account"})
        
    except Staff.DoesNotExist:
        return JsonResponse({"message": "We can't find an account associated with this email, kindly contact your employer"})
    


############# LOGIN ###############

@router.post("/login", response={200: LoginResponseSchema, 404: NotFoundSchema}, tags=["Manual Login"])
def post_login_view(request, data: EmailLoginRequestSchema):
    
    if "@" in data.email:
        user = authenticate(request, email=data.email, password=data.password)
        if user is not None:
            if data.remember_me and data.remember_me == True:
                remember_user = User.objects.get(email = user)
                remember_user.remember_me = True
                remember_user.save()
                # User is authenticated for 2 weeks if remember_me is true
                request.session.set_expiry(1209600) #2 weeks
                login(request, user)
                # Generate token here
                token = user.id  
                print(token)
                return HttpResponse(token)
                #return 200, EmailLoginResponse(token=token)
            else:
                # User is authenticated for only 1 hour, if otherwise.
                request.session.set_expiry(3600) # 60 minutes
        else:
            return 404, NotFoundSchema(message = "A User cannot login")
    elif "@" not in data.email:
        try:
            get_user = User.objects.get(phone_number = data.email)
            if get_user:
                user = authenticate(request, email=get_user.email, password=data.password)
                if user is not None:
                    if data.remember_me and data.remember_me == True:
                        remember_user = User.objects.get(email = request.user)
                        remember_user.remember_me = True
                        request.session.set_expiry(1209600) # 2 weeks here
                        login(request, user)
                        # Generate token here
                        token = user.id  
                        return 200, EmailLoginResponse(token=token)
                    else:
                        request.session.set_expiry(3600) # 60 minutes
                else:
                    return 404, NotFoundSchema(message = "B User cannot login")
            else:
                return 404, NotFoundSchema(message = "C User does not exist")
        except:
            return 404, NotFoundSchema(message = "D User cannot login")


  ############   SOCIAL ACCOUNT ENDPOINTS FOR SIGNUP  ############
  ####      GOOGLE ENDPOINTS FOR THE ACTORS ###########

@router.get("/google/{actor_type}", tags=["Social Auth"])
def google_auth(request: HttpRequest, actor_type:str):
    if actor_type == "customer":
        request.session["actor_type"] = actor_type
        callback_url = request.build_absolute_uri(reverse('google_callback'))
        adapter = GoogleOAuth2Adapter(request)
        return redirect("/accounts/google/login/")
    elif actor_type == "deliveryagent":
        request.session["actor_type"] = actor_type
        callback_url = request.build_absolute_uri(reverse('google_callback'))
        adapter = GoogleOAuth2Adapter(request)
        return redirect("/accounts/google/login/")
    elif actor_type == "chef":
        request.session["actor_type"] = actor_type
        callback_url = request.build_absolute_uri(reverse('google_callback'))
        adapter = GoogleOAuth2Adapter(request)
        return redirect("/accounts/google/login/")
    elif actor_type == "supplymanager":
        request.session["actor_type"] = actor_type
        callback_url = request.build_absolute_uri(reverse('google_callback'))
        adapter = GoogleOAuth2Adapter(request)
        return redirect("/accounts/google/login/")
    else:
        return render(request, "500.html")


# Not implemented yet, until the Facebook/Whatsapp integration has been resolved. Just a placeholder atm.
@router.get("/facebook", tags=["Social Auth"])
def facebook_auth(request: HttpRequest):
    callback_url = request.build_absolute_uri(reverse('facebook_callback'))
    #callback_url += f"?user_type={user_type}"
    adapter = FacebookOAuth2Adapter(request)
    return redirect(client.get_redirect_url(callback_url))


##########  PASSWORD MANAGEMENT ###################


 

#############  LOGOUT VIEW ############
@router.post("/logout", response= {404: NotFoundSchema}, tags=["Logout"])
@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")
    
# Still a placeholder until the Facebook/Whatsapp integration is resolved.
def verify_phonenumber(number: str):
    phonenumber_verification_token = generate_verificationcode()
    pass
    """send_mail(
        "Verify Phone Number",
        f"You made a request to verify your phone number for Merge-Africa account account\nHere is your 6-digit verification code\n{phonenumber_verification_token}\nIf you are not the one that initiated this, kindly ignore oe get back to us at merge.africa",
        "mergeafrica@merge.com",
        
    )"""
 