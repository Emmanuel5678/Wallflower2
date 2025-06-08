from django.contrib import admin
from . models import Categorie, Customer, Product, Order,Featured_Products
# Register your models here.
admin.site.register(Categorie)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Featured_Products)
admin.site.register(Order)
