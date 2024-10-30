from allauth.account.views import (
    SignupView,
)
from django import forms
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

# from world.models import City
from restaurants.forms import RegistrationForm

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


class RegistrationView(SignupView):
    form_class = RegistrationForm
    template_name = "restaurants/onboarding/registration.html"
    success_url = reverse_lazy("actor_redirect")

    # def get_form_class(self):
    #     return RegistrationForm
signup = RegistrationView.as_view()

# TODO: add this back, but currently not working



@method_decorator(
    login_required(login_url=reverse_lazy("account_login")), name="dispatch"
)
class EmailVerificationDoneView(generic.TemplateView):
    template_name = "restaurants/onboarding/email-verification-done.html"
