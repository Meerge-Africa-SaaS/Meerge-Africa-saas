from typing import Any

from allauth.account.views import (
    PasswordResetView as _PasswordResetView,
    PasswordResetDoneView as _PasswordResetDoneView,
    EmailVerificationSentView as _EmailVerificationSentView,
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView

from restaurants.models import Restaurant, Staff
from . import forms, models, serializers


@method_decorator(login_required, name="dispatch")
class ActorRedirect(generic.RedirectView):
    """
    This view redirects an actor to the page they are supposed to be on
    """

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if isinstance(user, Staff):
            return reverse("restaurants:dashboard", args=(user.restaurants.id,))
        # assume the user is a restaurant owner
        if user.groups.filter(name="Restaurant Owner").exists():
            # check if this user is among a restuarant's owners
            restaurant = Restaurant.objects.filter(owner__in=(user.id,)).first()
            if restaurant:
                return reverse("restaurants:dashboard", args=(restaurant.custom_link,))
            return reverse("restaurant_onboarding")
        return "/"


class EmailVerificationSentView(_EmailVerificationSentView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if "verification_email" not in request.session:
            return redirect("restaurant_signup")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.session["verification_email"]
        return context


class PasswordResetView(_PasswordResetView):
    """Forgot Password View."""

    def form_valid(self, form: forms.PasswordResetForm) -> HttpResponse:
        self.request.session["reset_email"] = form.cleaned_data["email"]
        return super().form_valid(form)


class PasswordResetDoneView(_PasswordResetDoneView):
    """Forgot Password Done View."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.session["reset_email"]
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if "reset_email" not in request.session:
            return redirect("account_reset_password")
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


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = serializers.CustomTokenRefreshSerializer # type: ignore

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except InvalidToken as e:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

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
