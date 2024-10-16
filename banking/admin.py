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
        
        
class AccountDetailAdmin(admin.ModelAdmin):
    form = AccountDetailAdminForm
    list_display = [
        "user",
        "bank",
        "created_at",
        "updated_at",
    ]
    
    readonly_fields = [
        "user",
        "bank",
        "account_number",
        "account_holder_name",
        "iban",
        "swift_code",
    ]
    
    
admin.site.register(models.Bank, BankAdmin)
admin.site.register(models.AccountDetail, AccountDetailAdmin)