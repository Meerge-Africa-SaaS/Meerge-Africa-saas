from ninja import Router
from .schema import SuccessMessageSchema, PasswordChangeRequestSchema, PasswordResetRequestSchema, NotFoundSchema
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from allauth.account.views import PasswordResetFromKeyView as allauthPasswordResetFromKeyView
from allauth.account.forms import ResetPasswordForm as allauthResetPasswordForm

from allauth.account.forms import ResetPasswordForm, ResetPasswordKeyForm

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
    
''' @p_router.post("/reset", response={200: SuccessMessageSchema, 404: NotFoundSchema}, tags=["Password management"])
def password_reset(request, data: PasswordResetRequestSchema):
    request = HttpRequest()
    request.POST = {
        "uidb36": uid
    } '''
    

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