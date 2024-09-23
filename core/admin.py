from django.contrib import admin
from django import forms
from unfold.admin import ModelAdmin
from . import models


# class UserAdminForm(forms.ModelForm):
#     class Meta:
#         model = models.User
#         fields = "__all__"


class UserAdmin(ModelAdmin):
    # form = UserAdminForm
    list_display = [
        "username",
        "email",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
        "id",
    ]


admin.site.register(models.User, UserAdmin)
