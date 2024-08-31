from datetime import datetime, timedelta
from django.conf import settings
from ninja.security import HttpBearer
import jwt

def create_token(user_id, expiry_period):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=int(expiry_period)),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return User.objects.get(id=payload['user_id'])
    except (jwt.DecodeError, User.DoesNotExist):
        return None

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        user = get_user_from_token(token)
        if user:
            return user