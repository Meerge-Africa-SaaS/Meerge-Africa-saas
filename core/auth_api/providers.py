from django.contrib.auth import get_user_model
from ninja import Router

User = get_user_model()
router = Router()

