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
from core.CustomFiles.CustomBackend import EmailAuthBackend, PhoneAuthBackend
from core.models import EmailVerification
from customers.models import Customer
from orders.models import DeliveryAgent
from banking.models import Bank, AccountDetail
from inventory.models import Supplier

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
    SupplierOnboardSchema,
    AAB
)
from .token_management import create_token, CustomRefreshToken

User = get_user_model()
router = Router()


@router.post("/deliveryagent-step1", tags=["Onboarding"], response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step1(request, data: DeliveryAgentOnboardStep1Schema, driver_license_DOC: Optional[UploadedFile], 
                                voters_card_DOC: Optional[UploadedFile], NIN_doc: UploadedFile = File(...),):
    if ((data.vehicle_type == "motorcycle") or (data.vehicle_type == "truck")) and not drivers_license_DOC:
            return 404, "Drivers license document is required for motorcycles and trucks."
    elif (data.vehicle_type == "bicycle") and not voters_card_DOC:
            return 404, "Voters card document/image is required for bitorcycles."
        
    try:
        DeliveryAgent.objects.get(email = data.email)
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    
    try:
        DeliveryAgent.objects.get(email = data.email).update(
            vehicle_type = data.vehicle_type, vehicle_brand = data.vehicle_brand, 
            plate_number = data.plate_number, drivers_license = drivers_license_DOC, 
            drivers_license_id = data.drivers_license_ID, voters_card = voters_card_DOC, 
            voters_number = data.voters_card_ID, nin_doc = NIN_doc, nin_number = NIN_ID
            )
        return 200, {"Driving details done"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}

@router.post("/deliveryagent-step2", tags=["Onboarding"], response={200: JWTLoginResponseSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step2(request, data: DeliveryAgentOnboardStep2Schema, face_capture: Optional[UploadedFile] = None):
    print(data.face_capture)
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
            work_shift = data.work_shift.dict(), face_capture = face_capture.image
            )
        return 200, {"Driving details done"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}
    
    
@router.post("/supplier", tags=["Onboarding"], response={200: SuccessMessageSchema, 400: NotFoundSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_supplier(request, data: Form[SupplierOnboardSchema], cac_document: UploadedFile = File(...), business_premise_license: Optional[UploadedFile] = None):
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
            cac_reg_number=data.cac_registration_number, cac_certificate=cac_document, business_license = business_premise_license, 
            category=data.category)
        return 200, {"message": "Supplier has been saved."}
        
    except Exception as e:
        return 400, {"message": e}
        