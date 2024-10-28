from django import forms
from django.contrib.auth.forms import (
    PasswordResetForm as _PasswordResetForm,
)
from allauth.account.forms import LoginForm

from . import models
from config.form_fields import PhoneNumberField


class UserSignupForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Enter your first name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name"}),
    )
    phone_number = PhoneNumberField(
        label="Phone Number",
    )

    def signup(self, request, user):
        ...


class UserSigninForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = ""


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            "email",
            "username",
        ]


class PasswordResetForm(_PasswordResetForm):
    """Forgot Password Form."""

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autofocus": True, "placeholder": "Enter your email address"}
        ),
    )
