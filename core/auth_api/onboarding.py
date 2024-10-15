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
from ninja import Form

from core.auth_api.schema import CustomerSignupRequestSchema
from core.CustomFiles.CustomBackend import EmailAuthBackend, PhoneAuthBackend
from core.models import EmailVerification
from customers.models import Customer
from orders.models import DeliveryAgent
from banking.models import Bank, AccountDetail

from .schema import (
    AcceptInvitation,
    AddEmployeeSchema,
    DeliveryAgentSignupRequestSchema,
    DeliveryAgentOnboardStep1Schema,
    DeliveryAgentOnboardStep2Schema,
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


@router.post("/deliveryagent-step1", tags=["Onboarding"], response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step1(request, data: DeliveryAgentOnboardStep1Schema = Form(...)):
    try:
        DeliveryAgent.objects.get(email = data.email)
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    try:
        DeliveryAgent.objects.get(email = data.email).update(vehicle_type = data.vehicle_type, vehicle_brand = data.vehicle_brand, 
                                                             plate_number = data.plate_number, drivers_license = data.drivers_license_doc, 
                                                             drivers_license_id = data.drivers_license_ID, voters_card = data.voters_card_doc, 
                                                             voters_number = data.voters_card_ID, nin_doc = data.NIN_doc, nin_number = data.NIN_ID)
        return 200, {"Driving details done"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}

@router.post("/deliveryagent-step2", tags=["Onboarding"], response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step2(request, data: DeliveryAgentOnboardStep2Schema = Form(...)):
    try:
        deliveryagent = DeliveryAgent.objects.get(email = data.email)
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    except Exception as e:
        return 500, {"message": "Error while querying user"}
    try:
        bank_model = Bank.objects.get_or_create(name = data.Bank_name, code = 1)
        account_details = AccountDetail.objects.create(
            user = deliveryagent, bank = bank_model, account_number = data.Bank_account_number, 
            account_holder_name = data.Bank_account_name
            )
        DeliveryAgent.objects.get(email = data.email).update(
            N_O_N_full_name = data.NON_full_name, N_O_N_phone_number = data.NON_phone_number, 
            guarantor_first_name = data.guarantor_first_name, guarantor_last_name = data.guarantor_last_name, 
            guarantor_occupation = data.guarantor_occupation, guarantor_phone_number = data.guarantor.phone_number,
            work_shift = data.work_shift.dict(), face_capture = data.face_capture.image
            )
        return 200, {"Driving details done"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}