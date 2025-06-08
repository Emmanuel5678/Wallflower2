from django.contrib import admin
from . models import PaymentTransaction
# Register your models here.


class PaymentsAdmin(admin.ModelAdmin):
  list_display = ('email', 'amount', 'status', 'created_at', 'reference', 'phone')

# Register the PaymentTransaction model with the admin class
    
admin.site.register(PaymentTransaction, PaymentsAdmin)
