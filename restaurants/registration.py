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
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from phonenumber_field.phonenumber import PhoneNumber

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

    def clean_phone_number(self) -> PhoneNumber:
        phone_number: PhoneNumber = self.cleaned_data["phone_number"]
        if User.objects.filter(
            phone_number=phone_number.as_e164.replace(" ", "")
        ).exists():
            raise forms.ValidationError("User with this phone number already exists.")
        return phone_number

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        if allauthEmailAddress.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")
        return email

    def clean(self) -> dict[str, Any]:
        return super().clean()

    def save(self, commit: bool = True) -> Any:
        self.instance.username = self.instance.email.split("@")[0]
        self.instance.set_password(self.cleaned_data["password"])
        self.instance.save()
        return self.instance


class RegistrationView(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("restaurant_email_verification_sent")
    template_name = "restaurants/onboarding/registration.html"

    def form_valid(self, form: forms.BaseModelForm) -> HttpResponse:
        user: User = form.save()
        # allauthemail_address = allauthEmailAddress.objects.create(
        #     user=user, email=user.email, verified=False, primary=True
        # )
        # send verification email
        # confirmation = allauthEmailConfirmation.create(allauthemail_address)
        # confirmation.send(self.request, signup=True)
        # messages.info(
        #     self.request,
        #     "A verification email has been sent to your email address. Please verify your email to continue",
        # )

        # log user in
        login(self.request, user=user)
        return super(generic.CreateView, self).form_valid(form)


# TODO: add this back, but currently not working
# @method_decorator(
#     login_required(login_url=reverse_lazy("core_User_signin")), name="dispatch"
# )
class EmailVerificationSentView(generic.TemplateView):
    template_name = "restaurants/onboarding/email-verification-sent.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if allauthEmailConfirmation.objects.filter(
            email_address__user=request.user
        ).exists():
            return super().get(request, *args, **kwargs)
        messages.error(
            self.request,
            "You have already verified your email address.",
        )
        return redirect("restaurant_onboarding")


class EmailVerificationDoneView(generic.TemplateView):
    template_name = "restaurants/onboarding/email-verification-done.html"
