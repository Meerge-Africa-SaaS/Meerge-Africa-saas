from ninja import Router
from ninja.security import HttpBearer

from .schema import DeliveryAgentSchema

router = Router()

def update_profile(data: DeliveryAgentSchema):
    pass