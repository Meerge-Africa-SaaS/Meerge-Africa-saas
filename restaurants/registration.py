import os

from django import forms
from django.urls import reverse_lazy
from django.views import generic
from phonenumber_field.formfields import PhoneNumberField

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


class SignupForm(forms.ModelForm):
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
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            add_placeholder(field, self)


class SignupView(generic.CreateView):
    form_class = forms.SignupForm
    success_url = reverse_lazy("login")
    template_name = "registration/restaurant/signup.html"
