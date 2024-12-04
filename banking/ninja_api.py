from django.contrib.auth import get_user_model
from ninja import Router
from typing import List
from banking.models import Bank, AccountDetail
from .schema import BankSchema, AccountDetailSchema
from core.auth_api.schema import SuccessMessageSchema, NotFoundSchema

router = Router()
User = get_user_model()

@router.post("/add-bank", tags=["Temp bank addition"], response={200: SuccessMessageSchema, 404: NotFoundSchema})
def add_bank(request, data: BankSchema):
    try:
        Bank.objects.create(name = data.name, code=data.code)
        return 200, "Bank object created"
        
    except Exception as e:
        return 404, "Can't create this bank object"
    
@router.get("/get-allbanks", tags=["Temp bank addition"], response={200: List[BankSchema], 404: NotFoundSchema})
def get_allbanks(request):
    try:
        banks = Bank.objects.all()
        return 200, banks
    
    except Exception as e:
        return 404, "Bank doesn't exist, add bank"
    

