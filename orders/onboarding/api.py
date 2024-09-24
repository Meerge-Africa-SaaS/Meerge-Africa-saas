from ninja import Router
from ninja.security import HttpBearer

from orders.models import DeliveryAgent
from .schema import OnboardDeliveryAgentSchema

router = Router()

@router.post("/onboarding", tags=['Onboarding'])
def update_profile(data: OnboardDeliveryAgentSchema):
    try:
        deliveryagent = DeliveryAgent.objects.get(email = data.email)
        deliveryagent.face_capture = data.face_capture
        deliveryagent.nin_doc = data.nin_doc
        deliveryagent.nin_number = data.nin_number
        deliveryagent.N_O_N_full_name = data.N_O_N_full_name
        deliveryagent.N_O_N_phone_number = data.N_O_N_phone_number
        deliveryagent.guarantor_first_name = data.guarantor_first_name
        deliveryagent.guarantor_last_name = data.guarantor_last_name
        deliveryagent.guarantor_phone_number = data.guarantor_phone_number
        deliveryagent.guarantor_occupation = data.guarantor_occupation
        if (data.vehicle_type == 'bicycle'):
            deliveryagent.vehicle_type = data.vehicle_type
            deliveryagent.vehicle_brand = data.vehicle_brand
            deliveryagent.voters_card = data.voters_card
            deliveryagent.voters_number = data.voters_number
        elif (data.vehicle_type == 'motorcycle' or data.vehicle_type == 'car' or data.vehicle_type == 'bus' or data.vehicle_type == 'truck'):
            deliveryagent.plate_number = data.plate_number
            deliveryagent.drivers_license = data.drivers_license
            deliveryagent.drivers_license_id = data.drivers_license_id
            deliveryagent.vehicle_brand = data.vehicle_brand
        else:
            return JsonResponse({"error": "Car vehicle type not allowed"})
                    
    except DeliveryAgent.DoesNotExist:
        return JsonResponse({"error": "This email does not exist in the delivery agent records"})
    
    except Exception:
        return JsonResponse({"error": "There is an error while saving your record, check your input"})