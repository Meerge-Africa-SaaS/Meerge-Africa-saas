from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models


class UserSigninView(auth_views.LoginView):
    next_page = "/"
    redirect_authenticated_user = False
    template_name = "core/user_signin.html"
    authentication_form = forms.UserSigninForm


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
