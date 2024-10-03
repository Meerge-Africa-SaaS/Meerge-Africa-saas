from django.contrib.auth import views as auth_views
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models


class UserSigninView(auth_views.LoginView):
    next_page = "/"
    redirect_authenticated_user = False
    template_name = "core/user_signin.html"
    authentication_form = forms.UserSigninForm


class PasswordResetView(auth_views.PasswordResetView):
    """Forgot Password View."""

    template_name = "core/password_reset/reset.html"
    form_class = forms.PasswordResetForm

    def form_valid(self, form: forms.PasswordResetForm) -> HttpResponse:
        self.request.session["reset_email"] = form.cleaned_data["email"]
        return super().form_valid(form)


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """Forgot Password Done View."""

    template_name = "core/password_reset/reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.session["reset_email"]
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if "reset_email" not in request.session:
            return redirect("password_reset")
        return super().get(request, *args, **kwargs)


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "core/password_reset/change.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Forgot Password Confirm View."""

    template_name = "core/password_reset/reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """Forgot Password Complete View."""

    template_name = "core/password_reset/reset_complete.html"

    def get(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        if "reset_email" in request.session:
            del request.session["reset_email"]
        return super().get(request, *args, **kwargs)


class UserListView(generic.ListView):
    model = models.User
    form_class = forms.UserForm


class UserCreateView(generic.CreateView):
    model = models.User
    form_class = forms.UserForm


class UserDetailView(generic.DetailView):
    model = models.User
    form_class = forms.UserForm


class UserUpdateView(generic.UpdateView):
    model = models.User
    form_class = forms.UserForm
    pk_url_kwarg = "pk"


class UserDeleteView(generic.DeleteView):
    model = models.User
    success_url = reverse_lazy("core_User_list")
