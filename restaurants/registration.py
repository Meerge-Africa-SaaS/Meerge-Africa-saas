from allauth.account.views import (
    SignupView,
)
from django import forms
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from allauth.account.utils import perform_login

# from world.models import City
from restaurants.forms import InvitationRegistrationForm, RegistrationForm
from restaurants.models import StaffInvitation

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


class InvitationRegistrationView(generic.FormView):
    template_name = "restaurants/onboarding/invitation-registration.html"
    success_url = reverse_lazy("actor_redirect")
    form_class = InvitationRegistrationForm

    def get_initial(self):
        initial = super().get_initial()
        initial["invite_key"] = self.kwargs["invite_key"]
        return initial

    def form_valid(self, form: InvitationRegistrationForm):
        staff = form.save(self.request)
        perform_login(self.request, staff, email_verification=True)
        return super().form_valid(form)
