from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Bank(models.Model):
    # Fields
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=10, primary_key=True)
    
    def __str__(self):
        return f"{self.name} - {self.code}"
    
    
    
class AccountDetail(models.Model):
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    
    # Fields
    account_number = models.CharField(max_length=128)
    account_holder_name = models.CharField(max_length=128)
    iban = models.CharField(max_length=34, blank=True, null=True)  # For international transfers
    swift_code = models.CharField(max_length=11, blank=True, null=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Account Detail"
        verbose_name_plural = "Account Details"
        unique_together = ('user', 'account_number')
        
    
    def __str__(self):
        return f"{self.bank.name} - {self.account_number}"
    