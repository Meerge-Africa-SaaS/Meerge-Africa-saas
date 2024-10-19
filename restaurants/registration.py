import os
from typing import Any

from django import forms
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from allauth.account.models import EmailAddress as allauthEmailAddress
from allauth.account.models import EmailConfirmation as allauthEmailConfirmation
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from phonenumber_field.phonenumber import PhoneNumber
from allauth.account.views import (
    SignupView,
    SignupForm,
)
from django.utils import timezone
from django.contrib.auth.models import Group


from config.form_fields import PhoneNumberField

# from world.models import City
from core.models import User

PLACEHOLDERS = {
    "first_name": "First Name",
    "last_name": "Last Name",
    "phone_number": "Enter Your Phone Number",
    "email": "Email Address",
    "password1": "Create your password",
    "password2": "Confirm your password",
}


def add_placeholder(field: str, form: forms.Form) -> None:
    form.fields[field].widget.attrs["placeholder"] = PLACEHOLDERS[field]


class RegistrationForm(SignupForm):
    def clean_phone_number(self) -> PhoneNumber:
        phone_number: PhoneNumber = self.cleaned_data["phone_number"]
        if User.objects.filter(
            phone_number=phone_number.as_e164.replace(" ", "")
        ).exists():
            raise forms.ValidationError("User with this phone number already exists.")
        return phone_number

    def clean(self):
        email = self.cleaned_data.get("email")
        if email:
            self.cleaned_data["username"] = email.split("@")[0]
        return super().clean()
    
    def signup(self, request: HttpRequest, user: User) -> None:
        user.phone_number = self.cleaned_data["phone_number"]
        owner_grp, _ = Group.objects.get_or_create(name="Restaurant Owner")
        user.groups.add(owner_grp)
        user.save()
        request.session["verification_email"] = user.email
        return super().signup(request, user)


class RegistrationView(SignupView):
    form_class = RegistrationForm
    template_name = "restaurants/onboarding/registration.html"
    success_url = reverse_lazy("actor_redirect")

    def get_form_class(self):
        return RegistrationForm


# TODO: add this back, but currently not working



@method_decorator(
    login_required(login_url=reverse_lazy("account_login")), name="dispatch"
)
class EmailVerificationDoneView(generic.TemplateView):
    template_name = "restaurants/onboarding/email-verification-done.html"
