from django.db import models
from wallflower.models import Product
# Create your models here.
#class Payments(models.Model):
  #first_name = models.CharField(max_length =50)
  #last_name = models.CharField(max_length =50)
  #email = models.EmailField()
  
  
  


class PaymentTransaction(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.email} - {self.amount}"
  