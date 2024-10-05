from typing import Any

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.contrib.auth.forms import (
    PasswordResetForm as _PasswordResetForm,
)

from . import models


class UserSigninForm(AuthenticationForm):
    username = None
    email = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))

    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.username_field = models.User._meta.get_field("email")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


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
