from django.db import models
import datetime

# Create your models here.
class Categorie(models.Model):
  name = models.CharField(max_length = 50)
  def __str__(self):
      return self.name
      
      
      
class Customer(models.Model):
  first_name = models.CharField(max_length = 50)
  last_name = models.CharField(max_length = 50)
  phone= models.CharField(max_length = 50)
  email = models.EmailField(max_length = 50)
  password = models.CharField(max_length = 50)
  def __str__(self):
      return f'{self.first_name}{self.last_name}'
      
      
      
class Product(models.Model):
  name = models.CharField(max_length = 50)
  price = models.CharField(max_length = 50)
  category = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=1)
  description= models.CharField(max_length = 250, default='', blank=True, null=True)
  image = models.ImageField(upload_to = 'uploads/product/')
  def __str__(self):
      return self.name
 
 
class Featured_Products(models.Model):
  name = models.CharField(max_length = 50)
  price = models.CharField(max_length = 50)
  category = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=1)
  description= models.CharField(max_length = 250, default='', blank=True, null=True)
  image = models.ImageField(upload_to = 'uploads/product/')
  def __str__(self):
      return self.name 
     
      
      
class Order(models.Model):
  Product= models.ForeignKey(Product, on_delete=models.CASCADE)
  Customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
  Quantity= models.IntegerField(default=1)
  Address= models.CharField(max_length = 250)
  Date= models.DateField(default= datetime.datetime.today)
  Status= models.BooleanField(default=False)
  def __str__(self):
      return self.Product
