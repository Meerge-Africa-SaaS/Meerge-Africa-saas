import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# External
from phonenumber_field.modelfields import PhoneNumberField
import secrets

USERNAME_REGEX = '^[a-zA-Z0-9.@_]*$'


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        user.is_active = user.is_admin = user.is_staff = user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser, AbstractBaseUser, PermissionsMixin):

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=256,
        unique=True,
    )
    username = models.CharField(
        db_index=True, verbose_name=_('username'), max_length=50, unique=True, blank=True, null=True,
        validators=[RegexValidator(regex=USERNAME_REGEX,
                                   message=_("Username must be Alpha-Numeric and may also contain '.', '@' and '_'."),
                                   code='Invalid Username.')],
        error_messages={
            "unique": _("A user with that username already exists."),
        },)
    phone_number = PhoneNumberField(
        blank=False, null=False, unique=True,
        verbose_name=_("phone number"),
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
        )
    

    class Meta:
        db_table = 'users'

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return str(self.pk)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        return reverse("core_User_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("core_User_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("core_User_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("core_User_htmx_delete", args=(self.pk,))



class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "email_verification_codes")
    email_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.user.email
    
class SmsVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "sms_verification_codes", blank=True, null=True)
    phone_number = PhoneNumberField()
    sms_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        if user:
            return self.user.email or self.user.phone_number or None
        else:
            return phone_number or None