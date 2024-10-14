from django.contrib import admin
from django import forms
from . import models

# Register your models here.
class BankAdminForm(forms.ModelForm):
    class Meta:
        model = models.Bank
        fields = "__all__"
        
        
class BankAdmin(admin.ModelAdmin):
    form = BankAdminForm
    list_display = [
        "name",
        "code"
    ]
    
    
class AccountDetailAdminForm(forms.ModelForm):
    class Meta:
        model = models.AccountDetail
        fields = "__all__"
        
        
class AccountDetailsAdmin(admin.ModelAdmin):
    form = AccountDetailAdminForm
    list_display = [
        "user",
        "bank",
        "created_at",
        "updated_at",
    ]
    
    readonly_fields = "__all__"
    
    
admin.site.register(models.Bank, BankAdmin)
admin.site.register(models.AccountDetail, AccountDetailsAdmin)