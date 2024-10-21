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
from django.core.files.storage import default_storage

from ninja import Router, File, UploadedFile, Form, Field
from ninja.security import HttpBearer

from typing import Optional

from core.auth_api.schema import CustomerSignupRequestSchema
from core.auth_api.token_management import AuthBearer
from core.CustomFiles.CustomBackend import EmailAuthBackend, PhoneAuthBackend
from core.models import EmailVerification
from customers.models import Customer
from orders.models import DeliveryAgent
from banking.models import Bank, AccountDetail
from inventory.models import Supplier

from .schema import (
    DeactivateAccountRequestSchema,
    DeliveryAgentSignupRequestSchema,
    DeliveryAgentOnboardStep1Schema,
    DeliveryAgentOnboardStep2Schema,
    EmailLoginRequestSchema,
    EmailVerificationSchema,
    JWTLoginResponseSchema,
    LoginResponseSchema,
    NotFoundSchema,
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
    SupplierOnboardSchema,
    AAB
)
from .token_management import create_token, CustomRefreshToken

User = get_user_model()
router = Router()


@router.put("/deliveryagent-step1", tags=["Onboarding"], response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step1(request, data: DeliveryAgentOnboardStep1Schema):
    
    try:
        DeliveryAgent.objects.get(email = data.email)
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    
    try:
        DeliveryAgent.objects.get(email = data.email).update(
            vehicle_type = data.vehicle_type, vehicle_brand = data.vehicle_brand, 
            plate_number = data.plate_number, drivers_license = data.drivers_license_DOC, 
            drivers_license_id = data.drivers_license_ID, voters_card = data.voters_card_DOC, 
            voters_number = data.voters_card_ID, nin_doc = data.NIN_doc, nin_number = data.NIN_ID
            )
        return 200, {"Driving details done"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}

@router.put("/deliveryagent-step2", tags=["Onboarding"], response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step2(request, data: DeliveryAgentOnboardStep2Schema):
    try:
        deliveryagent = DeliveryAgent.objects.get(email = data.email)
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    except Exception as e:
        return 500, {"message": "Error while querying user"}
    try:
        bank_model = Bank.objects.get_or_create(name = data.Bank_name, code = data.Bank_code)
        account_details = AccountDetail.objects.create(
            user = deliveryagent, bank = bank_model, account_number = data.Bank_account_number, 
            account_holder_name = data.Bank_account_name
            )
        DeliveryAgent.objects.get(email = data.email).update(
            N_O_N_full_name = data.NON_full_name, N_O_N_phone_number = data.NON_phone_number, 
            guarantor_first_name = data.guarantor_first_name, guarantor_last_name = data.guarantor_last_name, 
            guarantor_occupation = data.guarantor_occupation, guarantor_phone_number = data.guarantor.phone_number,
            work_shift = data.work_shift.dict(), face_capture = data.face_capture
            )
        return 200, {"Driving details done"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}
    
    
@router.put("/supplier", tags=["Onboarding"], response={200: SuccessMessageSchema, 400: NotFoundSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_supplier(request, data: SupplierOnboardSchema, ):
    try:
        supply_owner = User.objects.get(email = data.email)
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    except Exception as e:
        return 500, {"message": "Error while querying user"}
    
    try:
        if User.objects.filter(email = data.business_email).exists():
            return 404, {"message"}
        if Supplier.objects.filter(email = data.business_email).exists():
            return 404, {"mesage": "Email already exists"}
        
    except Exception as e:
        return 500, {"message": e}
    
    try:
        Supplier.objects.create(
            owner=supply_owner, name=data.business_name, email = data.business_email, phone_number = data.business_phone_number, 
            cac_reg_number=data.cac_registration_number, cac_certificate=data.cac_document, business_license = data.business_premise_license, 
            category=data.category)
        return 200, {"message": "Supplier has been saved."}
        
    except Exception as e:
        return 400, {"message": e}
        

@router.put("deactivate-my-account", auth=AuthBearer(), tags=["Deactivate Account"], response={200: SuccessMessageSchema, 400: NotFoundSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def deactivate_personal_account(request, data: DeactivateAccountRequestSchema):
    try:
        token = CustomRefreshToken(data.refresh_token)
        user = User.objects.get(id = token["user_id"])
        if user.is_authenticated:
            if user.check_password(data.password):
                token.blacklist()
                django_logout(request)
                user.is_active = False
                user.save()
                return 200, {"message": "User's account has been deactivated."}
            return 404, {"message": "Invalid Password"}
        return 404, {"message": "User need to be logged in before performing this action"}
        
    except Exception as e:
        return 404, {"message": "Invalid Token"}