from django import forms
from django.contrib.auth.forms import (
    PasswordResetForm as _PasswordResetForm,
)
from allauth.account.forms import LoginForm

from . import models


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
