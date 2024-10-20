from ninja import Schema, Field, File, ModelSchema, Form, UploadedFile
from typing import Optional, List, Any
from pydantic import BaseModel, constr, validator
from inventory.models import Supplier


email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
phone_number_regex = r'^\+?[1-9]\d{1,14}$'

# This userschema is used across other apps, not necessarily used only for the core app, so it makes sense to add it here, from which other apps can just use.
class UserSchema(Schema):
    first_name: str
    last_name: str
    email: str = Field(pattern = email_regex)
    phone_number: str = Field(pattern = phone_number_regex)
    

class RequestPhoneNumberVerificationSchema(Schema):
    phone_number: str = Field(pattern = phone_number_regex)

class SubmitPhoneNumberVerificationSchema(Schema):
    phone_number: str = Field(pattern = phone_number_regex)
    token: str

class EmailVerificationSchema(Schema):
    email: str = Field(pattern = email_regex)
    token: str

class ResendEmailCodeSchema(Schema):
    email: str = Field(pattern = email_regex)

##  SIGNUP SCHEMA #############
class SignupRequestSchema(Schema):
    first_name: str
    last_name: str
    email: str = Field(pattern = email_regex)
    phone_number: str = Field(pattern = phone_number_regex)
    password: str
    actor_type: str
    is_mobile: bool
    
class StaffSignupRequestSchema(Schema):
    first_name: str
    last_name: str
    email: str = Field(pattern = email_regex)
    phone_number: str = Field(pattern = phone_number_regex)
    password: str
    actor_type: str
    is_mobile: bool
    role: str
    works_at: str


class CustomerSignupRequestSchema(Schema):
    first_name: str
    last_name: str
    email: str = Field(pattern = email_regex)
    phone_number: str = Field(pattern = phone_number_regex)
    password: str
    actor_type: str
    
class CustomerSignupResponseSchema(Schema):
    user_id: int

class AddEmployeeSchema(Schema):
    email: str = Field(pattern = email_regex)
    role: str
    restaurant_name: str
    actor_type: str

class SocialAccountSignupSchema(Schema):
    email: str = Field(pattern = email_regex)
    password: str
    first_name: str
    last_name: str

class SignupResponseSchema(Schema):
    user_id: int

class AcceptInvitation(Schema):
    email: str = Field(pattern = email_regex)
    works_at: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    address: str

    
class StaffSignupResponseSchema(Schema):
    user_id: int  
    

class WorkShiftSchema(Schema):
    morning: List[str]
    afternoon: List[str]
    evening: List[str]

    @validator('morning', 'afternoon', 'evening')
    def validate_shift(cls, v):
        valid_days = set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        if not set(v).issubset(valid_days):
            raise ValueError('Invalid day in work shift')
        return v


class DeliveryAgentSignupRequestSchema(Schema):
    first_name: str
    last_name: str
    phone_number: str
    email: str = Field(pattern = email_regex)
    address: str
    password: str
    actor_type: str
    

class DeliveryAgentOnboardStep1Schema(Schema):
    email: str = Field(pattern = email_regex)
    vehicle_type: str
    vehicle_brand: str
    plate_number: Optional[str] = None
    drivers_license_ID: Optional[str] = None
    voters_card_ID: Optional[str] = None
    
    @validator('vehicle_type')
    def validate_vehicle_type(cls, vehicle):
        if vehicle not in ["bicycle", "motorcycle", "truck"]:
            raise ValueError("Vehicle type not accepted")
        return vehicle
    
    @validator("plate_number")
    def validate_plate_number(cls, _plate_number, values):
        if ((values.get("vehicle_type") == "motorcycle") or (values.get("vehicle_type") == "truck")) and not _plate_number:
            raise ValueError("Plate Number is required for motorcycles and trucks.")
    
    @validator("drivers_license_ID")
    def validate_drivers_license_ID(cls, _drivers_license_ID, values):
        if ((values.get("vehicle_type") == "motorcycle") or (values.get("vehicle_type") == "truck")) and not _drivers_license_ID:
            raise ValueError("Drivers License ID is required for motorcycles and trucks.")
    
    @validator("voters_card_ID")
    def validate_voters_card_ID(cls, _voters_card_ID, values):
        if (values.get("vehicle_type") == "bicycle") and not _voters_card_ID:
            raise ValueError("Voters card number is required for bicycles.")
    
    
class DeliveryAgentOnboardStep2Schema(Schema):
    email: str = Field(pattern = email_regex)
    NON_full_name: str
    NON_phone_number: str
    guarantor_first_name: str
    guarantor_last_name: str
    guarantor_occupation: str
    guarantor_phone_number: str
    Bank_name: str
    Bank_code: str
    Bank_account_number: str
    Bank_account_name: str
    work_shift: WorkShiftSchema
    
    @validator('work_shift')
    def validate_work_shift(cls, v):
        total_shifts = len(v.morning) + len(v.afternoon) + len(v.evening)
        if total_shifts < 6:
            raise ValueError('Must select at least 3 days in 2 out of 3 time periods')
        return v
    
    
class SupplierOnboardSchema(Schema):
    email: str = Field(pattern = email_regex)
    business_name: str
    business_email: str = Field(pattern = email_regex)
    business_phone_number: str
    business_address: str
    cac_registration_number: str
    category: str
     
    
class AAB(Schema):
    cac_document: UploadedFile

###########    LOGIN SCHEMA  #############
    
## Manual signup  ########
class LoginResponseSchema(Schema):
    token: str
    
class JWTLoginResponseSchema(Schema):
    refresh: str
    access: str
    user_id: str
    actor_type: str

class EmailLoginRequestSchema(Schema):
    email: str = Field(pattern = email_regex)
    password: str
    remember_me: Optional[bool|None]
 
class PhoneNumberVerificationRequestSchema(Schema):
     phone_number: str = Field(pattern = phone_number_regex)
     
 
class PhoneNumberLoginRequestSchema(Schema):
    phone_number: str
    password: str
    remember_me: Optional[bool|None]
    

class PhoneNumberLoginResponseSchema(Schema):
    token: str

class SocialLoginRequestSchema(Schema):
    access_token: str
    
class SuccessMessageSchema(Schema):
    message: str
    
class NotFoundSchema(Schema):
    message: str
    
class PasswordChangeRequestSchema(Schema):
    email: str = Field(pattern = email_regex)
    old_password: str
    new_password: str
    
class PasswordChangeRequestDoneSchema(Schema):
    email: str = Field(pattern = email_regex)
    token: str
    
class PasswordResetRequestSchema(Schema):
    email: str = Field(pattern = email_regex)
    
class PasswordResetRequestDoneSchema(Schema):
    email: str = Field(pattern = email_regex)
    token: str 
  