from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None