from datetime import timedelta as datetime_timedelta
import cloudinary.uploader

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
from django.db import transaction

from ninja import Router, File, Form, Field
from ninja.files import UploadedFile
from ninja.security import HttpBearer

from typing import Optional

from core.auth_api.schema import CustomerSignupRequestSchema
from core.auth_api.token_management import AuthBearer
from core.CustomFiles.CustomBackend import EmailAuthBackend, PhoneAuthBackend
from core.models import EmailVerification
from customers.models import Customer
from orders.models import DeliveryAgent
from banking.models import Bank, AccountDetail
from inventory.models import Supplier, Category
from restaurants.models import Restaurant

from .schema import (
    DeactivateAccountRequestSchema,
    DeliveryAgentSignupRequestSchema,
    DeliveryAgentOnboardStep1Schema,
    DeliveryAgentOnboardStep2Schema,
    DeliveryAgentOnboardStep3Schema,
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
    RestaurantOnboardStep1Schema,
    RestaurantOnboardStep2Schema,
    SignupRequestSchema,
    SignupResponseSchema,
    SocialAccountSignupSchema,
    SocialLoginRequestSchema,
    StaffSignupRequestSchema,
    StaffSignupResponseSchema,
    SuccessMessageSchema,
    SupplierOnboardSchema,
)
from .token_management import create_token, CustomRefreshToken

User = get_user_model()
router = Router()


def upload_media(media_file):
    try:
        file_upload = cloudinary.uploader.upload(media_file)
        file_url = file_upload["url"]
        
        return {"status": True, "data_url": file_url}
    except:
        return {"status": False, "data_url": None}


@router.post("/deliveryagent-step1", tags=["Onboarding"], auth=AuthBearer(), response={200: SuccessMessageSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step1(request, data: DeliveryAgentOnboardStep1Schema = Form(...), NIN_doc: UploadedFile = File(...), drivers_license_DOC: Optional[UploadedFile] = File(None), voters_card_DOC: Optional[UploadedFile] = File(None)):
    try:
        deliveryagent = DeliveryAgent.objects.get(id = request.auth["user_id"])
    except DeliveryAgent.DoesNotExist:
        return 404, {"message": "User does not exist"}
    
    if ((data.vehicle_type == "motorcycle") or (data.vehicle_type == "truck")) and not driver_license_DOC:
        return 404, {"message": "Drivers license document is required for motorcycles and trucks."}
    
    elif (data.vehicle_type == "bicycle") and not voters_card_DOC:
        return 404, {"message": "Voters card document/image is required for motorcycles."}
    
    try:
        nin_document = upload_media(NIN_doc)
        if nin_document["status"] == True:
            NIN_doc = nin_document["data_url"]
        else:
            return 404, {"message": "We ran into an error while uploading your nin document"}
    except:
        return 404, {"message": "Error in uploading NIN document"}
    
    try:
        if ((data.vehicle_type == "motorcycle") or (data.vehicle_type == "truck")):
            drivers_license_document = upload_media(drivers_license_DOC)
        if drivers_license_document["status"] == True:
            drivers_license_DOC = drivers_license_document["data_url"]
        else:
            return 404, {"message": "We ran into an error while uploading your drivers license document"}
    except:
        return 404, {"message": "Error in uploading drivers license document"}
    
    try:
        if (data.vehicle_type == "bicycle"):
            voters_card_document = upload_media(voters_card_DOC)
        if voters_card_document["status"] == True:
            voters_DOC = voters_card_document["data_url"]
        else:
            return 404, {"message": "We ran into an error while uploading your voters card document"}
    except:
        return 404, {"message": "Error in uploading voters card document"}
    
    try:
        deliveryagent.vehicle_type = data.vehicle_type
        deliveryagent.vehicle_brand = data.vehicle_brand 
        deliveryagent.plate_number = data.plate_number
        deliveryagent.drivers_license = drivers_license_DOC
        deliveryagent.drivers_license_id = data.drivers_license_ID
        deliveryagent.voters_card = voters_card_DOC
        deliveryagent.voters_number = data.voters_card_ID
        deliveryagent.nin_doc = NIN_doc
        deliveryagent.nin_number = data.NIN_ID
        deliveryagent.save()
            
        return 200, {"message": "Driving details registered"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}

@router.post("/deliveryagent-step2", tags=["Onboarding"], auth=AuthBearer(), response={200: SuccessMessageSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step2(request, data: DeliveryAgentOnboardStep2Schema):
    try:
        deliveryagent = DeliveryAgent.objects.get(id = request.auth["user_id"])
    except DeliveryAgent.DoesNotExist:
        return 404, {"message": "User does not exist"}
    except Exception as e:
        return 500, {"message": "Error while querying user"}
    try:
        deliveryagent.N_O_N_full_name = data.NON_full_name
        deliveryagent.N_O_N_phone_number = data.NON_phone_number
        deliveryagent.guarantor_first_name = data.guarantor_first_name
        deliveryagent.guarantor_last_name = data.guarantor_last_name
        deliveryagent.guarantor_occupation = data.guarantor_occupation
        deliveryagent.guarantor_phone_number = data.guarantor_phone_number
        deliveryagent.save()
        return 200, {"message": "Guarantor's details captured done"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}
    
@router.post("/deliveryagent-step3", tags=["Onboarding"], auth=AuthBearer(), response={200: SuccessMessageSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_deliveryagent_step3(request, data: DeliveryAgentOnboardStep3Schema, face_capture: File[UploadedFile]):
    try:
        deliveryagent = DeliveryAgent.objects.get(id = request.auth["user_id"])
    except DeliveryAgent.DoesNotExist:
        return 404, {"message": "User does not exist"}
    except Exception as e:
        return 500, {"message": "Error while querying user"}
    
    try:
        face_capture_document = upload_media(face_capture)
        if face_capture_document["status"] == True:
            face_capture = face_capture_document["data_url"]
        else:
            return 404, {"message": "We ran into an error while uploading your face capture"}
    except:
        return 404, {"message": "Error in uploading face capture"}
    
    try:
        deliveryagent.work_shift = data.work_shift.dict()
        deliveryagent.face_capture = face_capture
        deliveryagent.save()
      
        return 200, {"message": "Step 3 details captured"}
    except Exception as e:
        return 404, {"message": f"We ran into an error {e}"}
    
# Supplier onboarding endpoint/function
@router.post("/supplier", tags=["Onboarding"], auth=AuthBearer(), response={200: SuccessMessageSchema, 400: NotFoundSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_supplier(request, data: SupplierOnboardSchema, cac_document: UploadedFile = File(...), business_premise_license: Optional[UploadedFile] = File(None)):
    try:
        supply_owner = User.objects.get(id = request.auth["user_id"])
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    except Exception as e:
        return 500, {"message": "Error while querying user"}
    
    try:
        if User.objects.filter(email = data.business_email).exists():
            return 404, {"message": "Email has been used for personal account."}
        if Supplier.objects.filter(email = data.business_email).exists() or Restaurant.objects.filter(email = data.business_email).exists():
            return 404, {"mesage": "Email already exists"}
        
    except Exception as e:
        return 500, {"message": e}
    
    try:
        supplier = Supplier.objects.create(
            owner=supply_owner, name=data.business_name, email = data.business_email, phone_number = data.business_phone_number, 
            cac_reg_number=data.cac_registration_number, cac_certificate=cac_document, business_license = business_premise_license, 
            )
        try:
            category_instances = Category.objects.filter(id__in = data.category)
            supplier.category.set(category_instances)
            supplier.save()
               
        except Exception as e: 
            return 404, {"message": "Category not captured correctly."}
        return 200, {"message": "Supplier has been saved."}
        
    except Exception as e:
        return 400, {"message": e}
     
# Restaurant onboarding endpoint/function
@router.post("/restaurant_onboard-step1", tags=["Onboarding"], auth=AuthBearer(), response={200: SuccessMessageSchema, 400: NotFoundSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_restaurant_step1(request, data: RestaurantOnboardStep1Schema):
    try:
        restaurant_owner = User.objects.get(id = request.auth["user_id"])
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    except Exception as e:
        return 500, {"message": "Error while querying user"}
    
    try:
        if User.objects.filter(email = data.business_email).exists():
            return 404, {"message": "Email has been used for personal account."}
        if Restaurant.objects.filter(email = data.business_email).exists() or Supplier.objects.filter(email = data.business_email).exists():
            return 404, {"mesage": "Email already exists"}
        
    except Exception as e:
        return 500, {"message": e}
    
    try:
        restaurant = Restaurant.objects.create(
            owner=restaurant_owner, email=data.business_email, name=data.business_name, phone_number = data.business_phone_number,
            address=data.business_address, business_category=data.business_category
        )
        return 200, {"message", f"Restaurant onboarding step 1 has been done. Restaurant ID = {restaurant.id}"}
        
    except Exception as e:
        return 404, {"message": "Error in onboarding a new restaurant"}
    

@transaction.atomic
@router.post("/restaurant_onboard-step2", tags=["Onboarding"], auth=AuthBearer(), response={200: SuccessMessageSchema, 400: NotFoundSchema, 404: NotFoundSchema, 500: NotFoundSchema})
def onboard_restaurant_step2(request, data: RestaurantOnboardStep2Schema, cac_document: Optional[UploadedFile] = File(None), business_premise_license: Optional[UploadedFile] = File(None)):
    if (data.business_registration_status == "registered" and not cac_document):
        return 404, {"message": "CAC document is required for registered restaurants"}
    
    try:
        restaurant_owner = User.objects.get(id = request.auth["user_id"])
    except User.DoesNotExist:
        return 404, {"message": "User does not exist"}
    except Exception as e:
        return 500, {"message": "Error while querying user"}
    
    try:
        restaurant = Restaurant.objects.get(id=data.restaurant_id)
    except Restaurant.DoesNotExist:
        return 404, {"message": "Restaurant does not exist"}
    
    try:
        with transaction.atomic():
            if cac_document:
                try:
                    cac_document_file = upload_media(cac_document)
                    if cac_document_file["status"] == True:
                        cac_document = cac_document_file["data_url"]
                    else:
                        return 404, {"message": "We ran into an error while uploading your cac document"}
                except:
                    return 404, {"message": "Error in uploading cac document"}
            if business_premise_license:
                try:
                    business_premise_license_file = upload_media(business_premise_license)
                    if business_premise_license_file["status"] == True:
                        business_premise_license = business_premise_license_file["data_url"]
                    else:
                        return 404, {"message": "We ran into an error while uploading your business premise license document"}
                except:
                    return 404, {"message": "Error in uploading business premise license document"}
                
            restaurant.business_reg_details = data.business_registration_status
            restaurant.cac_reg_number = data.cac_registration_number
            restaurant.cac_certificate = cac_document
            restaurant.business_license = business_premise_license
            restaurant.save()
            
    except Exception as e:
        return 500, {"message": "We ran into error while process your request."}
            
        

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