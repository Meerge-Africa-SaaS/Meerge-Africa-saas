from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


from customers.models import Customer
from orders.models import DeliveryAgent
from restaurants.models import Chef, Staff
from inventory.models import SupplyManager

class MyCustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        
        print("\n"*10)
        user = sociallogin.user
        print("HERE", request.session, "HERE AGAIN")
        print("POSTING THE REQQUEST HERE "*5)
        print(request)
        print("\n"*5)
        if not user.id:
            user.email = sociallogin.account.extra_data.get('email')
            user.first_name = sociallogin.account.extra_data.get('given_name', '')
            user.last_name = sociallogin.account.extra_data.get('family_name', '')
            user.username = user.email
            
            actor_type = request.POST.get("actor_type")
            address = request.POST.get("address")
            try:
                phone_number = request.POST.get("phone_number")
            except Exception:
                pass
            
            print("\n"*5,)
            if actor_type == "customer":
                customer = Customer.objects.update_or_create(username=user.username, email=user.email, address=address)
            
            elif actor_type == "delivery_agent":
                deliveryagent = DeliveryAgent.objects.create(username=user.username, email=user.email, address=address)
            
            elif actor_type == "chef":
                chef = Chef.objects.create(username=user.username, email=user.email, address=address)
                
            elif actor_type == "supply_manager":
                supplymanager = SupplyManager.objects.create(username=user.username, email=user.email, address=address)
            
            elif actor_type == "owner":
                business_owner = User.objects.create(username = user.username, email = user.email, address = user.address)
                
        else:
            print("From the else part", user.id)
        
    ''' def save_user(self, request, sociallogin, form=None):
        
        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form)
        else:
            get_account_adapter().populate_username(request, u)
        sociallogin.save(request)
        return u '''