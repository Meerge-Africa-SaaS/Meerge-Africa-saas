from ninja import Router
from .schema import SuccessMessageSchema, PasswordChangeRequestSchema, PasswordResetRequestSchema, NotFoundSchema
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from allauth.account.views import PasswordResetFromKeyView as allauthPasswordResetFromKeyView
from allauth.account.forms import ResetPasswordForm as allauthResetPasswordForm

from allauth.account.forms import ResetPasswordForm, ResetPasswordKeyForm

p_router = Router()
User = get_user_model()


class CustomPasswordResetFromKeyView(allauthPasswordResetFromKeyView):
    template_name = None
    success_url = None
    reset_url_key = "set-password"


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
    request = HttpRequest()
    request.POST = {
        "uidb36": uid,
        "key": token,
        "password1": new_password,
        "password2": new_password
    }
    #view = allauthPasswordResetFromKeyView.as_view()
    view = CustomPasswordResetFromKeyView.as_view()
    response = view(request)
    if response.status_code == 302:
        return JsonResponse({'message': "Password reset successful"})
    else:
        return JsonResponse({"message": "Invalid credentials"})