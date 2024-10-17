from ninja import Router
from .schema import SuccessMessageSchema, PasswordChangeRequestSchema, PasswordResetRequestSchema, PasswordResetRequestDoneSchema, NotFoundSchema, EmailLoginRequestSchema
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils import timezone as django_timezone
from allauth.account.views import PasswordResetFromKeyView as allauthPasswordResetFromKeyView
from allauth.account.forms import ResetPasswordForm as allauthResetPasswordForm
from allauth.account.forms import ResetPasswordForm, ResetPasswordKeyForm

from core.models import EmailVerification
from .token_management import generate_code

p_router = Router()
User = get_user_model()


class CustomPasswordResetFromKeyView(allauthPasswordResetFromKeyView):
    template_name = None
    success_url = None
    #reset_url_key = "set-password"


@p_router.post("/change", response = SuccessMessageSchema, tags=["Password management"])
@login_required
def password_change(request, data: PasswordChangeRequestSchema):
    #user = request.auth
    email = data.email
    old_password = data.old_password
    new_password = data.new_password
    
    user = User.objects.get(email = email)
    if user and user.is_authenticated:
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return 200, SuccessMessageSchema(message = "Password changed")
        
        else:
            return 404, NotFoundSchema(message = "Incorrect password")
    else:
        return 404, NotFoundSchema(message = "User needs to login before being allowed to change password.")
    
    
@p_router.post("/reset", response={200: SuccessMessageSchema, 404: NotFoundSchema}, tags=["Password management"])
def password_reset(request, data: PasswordResetRequestSchema):
    try:
        user = User.objects.get(email = data.email)
        if user and user.is_active:
            email_instance = EmailVerification.objects.filter(user = user).exists()
            token = generate_code()
            if not email_instance:
                email_token = EmailVerification.objects.create(user = user, email_code=token, created_at=django_timezone.now(), expires_at=django_timezone.now() + django_timezone.timedelta(minutes = 10))
            else:
                EmailVerification.objects.get(user).delete()
                email_token = EmailVerification.objects.create(user = user, email_code=token, created_at=django_timezone.now(), expires_at=django_timezone.now() + django_timezone.timedelta(minutes = 10))
            
            subject =  "Password Reset"
            message = f"""
                    Hello, here is your one time password reset email verification code {email_token.email_code}
                    """
            email_sender ="dev@kittchens.com"
            receiver = [data.email]
            try:
                send_mail(subject, message, email_sender, receiver)
                return 200, {
                    "message": "Password reset mail sent."
                }
            except Exception:
                return 404, {
                    "message": "Error in sending password reset mail"
                }
        elif not user.is_active:
            return 404, {
                "message": "Inactive profile, kindly proceed to verify your account."
            }
                
    except User.DoesNotExist:
        return 404, {
            "message": "User does not exist"
        }
        
    except Exception as e:
        print(e)
        return 404, {
            "message": "We ran into error while processing your request."
        }
        

@p_router.post("/reset-done", response={200: SuccessMessageSchema, 404: NotFoundSchema}, tags=["Password, management"])
def password_reset_done(request, data: PasswordResetRequestDoneSchema):
    try:
        user_model = User.objects.get(email = data.email)
        email_instance = EmailVerification.objects.get(user=user_model)
        
        if email_instance.expires_at > django_timezone.now():
            if email_instance.email_code == data.token:
                email_instance.delete()
                return 200, {
                    "message": "Email verified. User can proceed to set new password"
                }
            else:
                return 404, {
                    "message": "Invalid token"
                }
        else:
            return 404, {
                "message": "Password reset token validity timeout, Kindly reset new password"
            }
    except User.DoesNotExist:
        return 404, {
            "message": "User does not exist"
        }
    except Exception as e:
        print(e)
        return 404, {
            "message": "We ran into error while processing your request."
        }
    

@p_router.post("/set-password", response={200: SuccessMessageSchema, 404: NotFoundSchema}, tags=["Password management"])
def set_password(request, data: EmailLoginRequestSchema):
    try:
        user = User.objects.get(email = data.email)
        user.set_password(data.password)
        user.save()
        return 200, {
            "message": "Password has been reset, proceed to login"
        }
        
    except User.DoesNotExist:
        return 404, {
            "message": "User does not exist"
        }
    
    

    
''' @p_router.post("/reset", response={200: SuccessMessageSchema, 404: NotFoundSchema}, tags=["Password management"])
def password_reset(request, data: PasswordResetRequestSchema):
    request = HttpRequest()
    request.POST = {
        "uidb36": uid
    } '''
    
''' 
@p_router.post("/reset", tags=["Password management"])
def password_reset(request, email: str):
    try:
        user = User.objects.get(email = email)
        form = allauthResetPasswordForm({
            "email": email
        })
        if form.is_valid():
            form.save(request = request)
            return JsonResponse({"message": "password sent"})
        else:
            return JsonResponse({"message": "error in form"})
    except User.DoesNotExist:
        return JsonResponse({"message": "User does not exist"})
    
    
@p_router.post("/reset/done")
def password_reset_done(request, uid: str, token: str, new_password: str):
    #new_request = HttpRequest()
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        form = ResetPasswordKeyForm(user, {"password1": new_password, "password2": new_password})
        if form.is_valid():
            form.save()
            return {"message": "Password reset successfully."}
    return {"message": "Invalid reset token."}
 '''
''' new_request.POST = {
        "uidb36": uid,
        "key": token}
    '' ,
        "password1": new_password,
        "password2": new_password
    } ''
    #view = allauthPasswordResetFromKeyView.as_view()
    view = CustomPasswordResetFromKeyView.as_view()
    response = view(new_request)
    if response.status_code == 302:
        return JsonResponse({'message': "Password reset successful"})
    else:
        return JsonResponse({"message": "Invalid credentials"}) '''