from ninja import Schema

class BankSchema(Schema):
    name: str
    code: str
    
    
class AccountDetailSchema(Schema):
    user_email: str
    