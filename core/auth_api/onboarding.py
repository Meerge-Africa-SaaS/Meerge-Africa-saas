from datetime import timedelta as datetime_timedelta

from cities_light.models import Country
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models.signals import post_save

from django.utils import timezone as django_timezone
from django.utils.http import urlsafe_base64_decode
from ninja import Router
from ninja.security import HttpBearer

from core.auth_api.schema import CustomerSignupRequestSchema
from core.CustomFiles.CustomBackend import EmailAuthBackend, PhoneAuthBackend
from core.models import EmailVerification
from customers.models import Customer
from orders.models import DeliveryAgent

from .schema import (
    AcceptInvitation,
    AddEmployeeSchema,
    DeliveryAgentSignupRequestSchema,
    EmailLoginRequestSchema,
    EmailVerificationSchema,
    JWTLoginResponseSchema,
    LoginResponseSchema,
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
from .token_management import create_token, CustomRefreshToken

User = get_user_model()
router = Router()


@router.post("/onboard-deliveryagent", response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent(request, data: )