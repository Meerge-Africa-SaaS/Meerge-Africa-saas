from django.contrib.auth import get_user_model
from django.db import transaction
from ninja import Router
from allauth.socialaccount.models import SocialToken, SocialAccount
from schema import SocialAuthSchema, AuthResponseSchema, NotFoundSchema

from customers.models import Customer
from orders.models import DeliveryAgent

import requests
from .token_management import create_token, CustomRefreshToken, generate_code

User = get_user_model()
router = Router()

def get_google_details(access_token):
    response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    if response.status_code == 200:
        return response.json()
    return None

def get_facebook_details(access_token):
    response = requests.get(
        'https://graph.facebook.com/me',
        params={
            'fields': 'id,email,first_name,last_name',
            'access_token': access_token
        }
    )
    if response.status_code == 200:
        return response.json()
    return None
    

@router.post('/social/google/authenticate', response={200: AuthResponseSchema, 404: NotFoundSchema})
@transaction.atomic
def google_authenticate(request, data: SocialAuthSchema):
    access_token = data.access_token
    actor_type = data.actor_type
    provider = "google"
    
    user_info = get_google_details(access_token)
    if not user_info:
        return 404, {"message": "Invalid token"}
    
    user_email = user_info["email"]
    if not user_email:
        return 404, {"message": "Email not found"}
    
    user_exists = User.objects.filter(email = user_email).exists()
    
    with transaction.atomic():
        if user_exists:
            # Login flow
            user = User.objects.get(email=user_email)
            # Update social token if needed
            social_account = SocialAccount.objects.filter(user=user, provider=provider).first()
            if social_account:
                SocialToken.objects.update_or_create(
                    account=social_account,
                    defaults={'token': access_token}
                )
        else:
            # Signup flow
            if actor_type == "owner":
                user = User.objects.create_user(
                    email=user_email,
                    username=user_email,
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', '')
                )
                
            elif actor_type == "customer":
                user = Customer.objects.create(
                    email=user_email,
                    username=user_email,
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', '')
                )
                
            elif actor_type == "deliveryagent":
                user = DeliveryAgent.objects.create(
                    email=user_email,
                    username=user_email,
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', '')
                )
                
            else:
                return 404, {"message": "Invalid actor type"}
                
            # Create social account
            social_account = SocialAccount.objects.create(
                provider=provider,
                uid=user_info.get('sub'),
                user=user
            )
            
            # Create social token
            SocialToken.objects.create(
                account=social_account,
                token=access_token
            )
        
            token_expiry_period, access_token_period = 7, 600
            token = CustomRefreshToken.for_user(str(user))
            token.set_exp(lifetime=datetime_timedelta(days=token_expiry_period))
            access_token = token.access_token
            access_token.set_exp(lifetime=datetime_timedelta(minutes=access_token_period))
            
            user.last_login = django_timezone.now()
            user.save(update_fields=['last_login'])
            
            return 200, {
                "refresh": str(token),
                "access": str(access_token),
                "user_id": str(user),
                "actor_type": actor_type,
                "is_new_user": not user_exists
            }


