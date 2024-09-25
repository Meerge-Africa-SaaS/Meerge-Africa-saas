from ninja import Schema, File
from ninja.files import UploadedFile
from typing import Optional
from pydantic import Field, root_validator, ValidationError

phone_number_regex = r'^\+?[1-9]\d{1,14}$'

class OnboardDeliveryAgentSchema(Schema):
    email: str
    face_capture: UploadedFile = File(...)
    vehicle_type: str
    vehicle_brand: str
    plate_number: Optional[str] = None
    drivers_license: Optional[UploadedFile] = Field(None)
    drivers_license_id: Optional[str] = None
    voters_card: Optional[UploadedFile] = Field(None)
    voters_number: Optional[str] = None
    nin_doc: UploadedFile = File(...)
    nin_number: str
    N_O_N_full_name: str
    N_O_N_phone_number: str = Field(pattern = phone_number_regex)
    guarantor_first_name: str
    guarantor_last_name: str
    guarantor_phone_number: str = Field(pattern = phone_number_regex)
    guarantor_occupation: str
    address: str
    
    @root_validator(pre=True)
    def check_dependent_fields(cls, values):
        vehicle_type = values.get('vehicle_type')
        plate_number = values.get('plate_number')
        drivers_license = values.get('drivers_license')
        drivers_license_id = values.get('drivers_license_id')
        voters_card = values.get('voters_card')
        voters_number = values.get('voters_number')
        if (vehicle_type == 'bicycle') and (not voters_card or not voters_number):
            raise ValueError('Fields: voters_card and voters_number is required when vehicle_type = bicycle')
        if (vehicle_type == 'motorcycle' or vehicle_type == 'car' or vehicle_type == 'bus' or vehicle_type == 'truck') and (not plate_number or not drivers_license or not drivers_license_id):
            raise ValueError('Field:  plate_number, drivers_license, drivers_license_id is required when vehicle type is any of [motorycycle, car, bus, truck]')
        
        return values