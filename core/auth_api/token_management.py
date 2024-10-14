from datetime import datetime, timedelta, timezone
from django.conf import settings
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import EmailVerification
import jwt
from random import randint

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        user_model = User.objects.get(id = user)
        token = super().for_user(user_model)
        token['name'] = user_model.get_full_name()
        token['user_id'] = str(user_model)
        token['email'] = user_model.email
        
        return token
    

def generate_code():
    token = ""
    for i in range(0,6):
        token += str(randint(0,9))
        
    return token
            

    
def create_token(user_id, expiry_period):
    issued_day = datetime.now(tz=timezone.utc)
    expiry_day = datetime.now(tz=timezone.utc) + timedelta(days=int(expiry_period))
    
    payload = {
        'user_id': user_id,
        'exp': expiry_day,
        'iat': issued_day,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return User.objects.get(id=str(payload['user_id']))
    except (jwt.DecodeError, User.DoesNotExist):
        return None
    except Exception:
        return None
    

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        user = get_user_from_token(token)
        if user:
            return user
        
        