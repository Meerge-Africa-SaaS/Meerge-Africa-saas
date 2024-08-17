from ninja import Schema
from typing import Optional
from pydantic import constr, Field

''' class EmailVerificationSchema(Schema):
    email: str
    ''' 

# This userschema is used across other apps, not necessarily used only for the core app, so it makes sense to add it here, from which other apps can just use.
class UserSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone_number: str = Field(pattern = r'^\+?[1-9]\d{1,14}$')
    #phone_number: constr(regex=r'^\+?[1-9]\d{1,14}$')
    
class CustomerSignup(Schema):
    pass

class RequestPhoneNumberVerificationSchema(Schema):
    phone_number: str = Field(pattern = r'^\+?[1-9]\d{1,14}$')

class SubmitPhoneNumberVerificationSchema(Schema):
    phone_number: str = Field(pattern = r'^\+?[1-9]\d{1,14}$')
    token: str

class EmailVerificationSchema(Schema):
    email: str
    token: str

class ResendEmailCodeSchema(Schema):
    email: str

##  SIGNUP SCHEMA #############
class SignupRequestSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone_number: str = Field(pattern = r'^\+?[1-9]\d{1,14}$')
    password: str
    username: Optional[str] = None
    actor_type: str
    is_mobile: bool

class SocialAccountSignupSchema(Schema):
    email: str
    password: str
    first_name: str
    last_name: str

class SignupResponseSchema(Schema):
    user_id: int

class AddEmployeeSchema(Schema):
    email: str
    role: str
    restaurant_name: str
    
class AcceptInvitation(Schema):
    email: str
    works_at: str
    first_name: str
    last_name: str
    username: str
    phone_number: str
    password: str
    address: str

class StaffSignupRequestSchema(Schema):
    email: str
    username: str
    phone_number: str
    password: str
    works_at: str
    
class StaffSignupResponseSchema(Schema):
    user_id: int  
    


###########    LOGIN SCHEMA  #############
    
## Manual signup  ########
class LoginResponseSchema(Schema):
    token: str
    
class EmailLoginRequestSchema(Schema):
    email: str
    password: str
    remember_me: Optional[bool|None]

 
class PhoneNumberLoginRequestSchema(Schema):
    phone_number: str
    password: str

class PhoneNumberLoginResponseSchema(Schema):
    token: str

class SocialLoginRequestSchema(Schema):
    access_token: str
    
class SuccessMessageSchema(Schema):
    message: str
    
class NotFoundSchema(Schema):
    message: str
    
class PasswordChangeRequestSchema(Schema):
    email: str
    old_password: str
    new_password: str
    
class PasswordChangeRequestDoneSchema(Schema):
    email: str
    token: str
    
class PasswordResetRequestSchema(Schema):
    email: str
    
class PasswordResetRequestDoneSchema(Schema):
    email: str
    token: str
    
