import os
from typing import Any

from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic

from config.form_fields import PhoneNumberField

# from world.models import City
from core.models import User

PLACEHOLDERS = {
    "first_name": "First Name",
    "last_name": "Last Name",
    "phone_number": "Enter Your Phone Number",
    "email": "Email Address",
    "password": "Create your password",
}


def add_placeholder(field: str, form: forms.Form) -> None:
    form.fields[field].widget.attrs["placeholder"] = PLACEHOLDERS[field]


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        ]
        field_classes = {
            "phone_number": PhoneNumberField,
        }
        widgets = {
            "password": forms.PasswordInput(
                attrs={
                    "autocomplete": "new-password",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            add_placeholder(field, self)

    def clean(self) -> dict[str, Any]:
        return super().clean()

    def save(self, commit: bool = True) -> Any:
        self.instance.username = self.instance.email
        user = super().save(commit)
        self.instance.set_password(self.cleaned_data["password"])
        self.instance.save()
        return user


class RegistrationView(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("core_User_signin")
    template_name = "restaurants/onboarding/registration.html"

    def form_valid(self, form: forms.BaseModelForm) -> HttpResponse:
        messages.success(
            self.request,
            "Your account has been created successfully. Please login to continue",
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return super().get_success_url() + "?next=" + reverse("restaurant_onboarding")
