from django.shortcuts import render, redirect
from . models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.generic import ListView, TemplateView
from django.conf import settings
import requests
from django.urls import reverse
# Create your views here.

def home(request):
  products= Product.objects.all()
  return render(request, 'home.html', {'products': products})
 
 
def about(request):
  return render(request, 'about.html')
  
def contact(request):
  return render(request, 'contact.html')
  
def services(request):
  return render(request, 'services.html')
  
  

def gallery(request):
   return render(request, 'gallery.html')
   
def custom_order(request):
   return render(request, 'custom_order.html')



@login_required(login_url='/wallflower/login/')
def shop(request):
  products= Product.objects.all()
  return render(request, 'shop.html', {'products': products})
  
def login_user(request):
  if request.method == 'POST':
     username = request.POST ['username']
     password = request.POST['password']
     user = authenticate(request, username=username, password=password)
     if user is not None:
        login(request, user)
        messages.success(request, ('You have successfully logged in'))
        return redirect ('wallflower:shop')
     else:
       messages.success(request, ('Incorrect password or username  '))
       return redirect ('wallflower:login')
  else:
  
  
  
  
  
  
  
  
  
     return render(request, 'login.html')
  
def logout_user(request):
  logout(request)
  messages.success(request, ('You have successfully logged out'))
  return redirect('wallflower:home')
  
  
  
  
def signup(request):
  if request.method == 'POST':
     #username = request.POST.get('username')
     username = request.POST['username']
     fname = request.POST['fname']
     lname = request.POST['lname']
     email = request.POST['email']
     pass1 = request.POST['pass1']
     pass2 = request.POST['pass2']
     
     if User.objects.filter(username=username):
       messages.error(request, 'Username Already Exists')
       return redirect('wallflower:home')
       
     if User.objects.filter(email= email):
       messages.error(request, 'Email Already Exists')
       return redirect('wallflower:home')
      
     if len(username)>10:
       messages.error(request, 'Length of username must not be more than 10')
       
       
     if pass1 != pass2:
       messages.error(request, "Passwords didn't match")
       
     if not username.isalnum():
       messages.error(request, 'Username Must be Alphanumeric')
       return redirect('wallflower:home')
       
       
       
     
       
       
      
     
     
     myuser = User.objects.create_user(username, email, pass1)
     myuser.first_name = fname
     myuser.last_name = lname
     
     myuser.save()
     
     messages.success(request, 'Your Account has been successfully created')
     
      
     
     return redirect ('wallflower:login')
     
     
  
  
  
  
  
    #form= UserCreationForm()
  return render(request, 'signup.html')
  
  
  
    














class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_featured=True)[:3]
        return context

class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply filters
        category = self.request.GET.get('category')
        price = self.request.GET.get('price')
        sort = self.request.GET.get('sort')
        
        if category:
            queryset = queryset.filter(category=category)
        
        if price == 'under-10000':
            queryset = queryset.filter(price__amount__lt=10000)
        elif price == '10000-20000':
            queryset = queryset.filter(price__amount__gte=10000, price__amount__lte=20000)
        elif price == '20000-30000':
            queryset = queryset.filter(price__amount__gt=100, price__amount__lte=30000)
        elif price == ' 30000-plus':
            queryset = queryset.filter(price__amount__gt=30000)
        
        if sort == 'price-low':
            queryset = queryset.order_by('price__amount')
        elif sort == 'price-high':
            queryset = queryset.order_by('-price__amount')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:  # featured
            queryset = queryset.order_by('-is_featured')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category')
        context['selected_price'] = self.request.GET.get('price')
        context['selected_sort'] = self.request.GET.get('sort')
        return context

class CustomOrderView(TemplateView):
    template_name = 'custom_order.html'
    
    def post(self, request, *args, **kwargs):
        # Process form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        jewelry_type = request.POST.get('jewelry_type')
        design_description = request.POST.get('design_description')
        measurements = request.POST.get('measurements')
        material_preference = request.POST.get('material_preference')
        deadline = request.POST.get('deadline')
        budget_range = request.POST.get('budget_range')
        special_requests = request.POST.get('special_requests')
        reference_images = request.FILES.getlist('reference_images')
        
        # Create custom order
        order = CustomOrder.objects.create(
            name=name,
            email=email,
            phone=phone,
            jewelry_type=jewelry_type,
            design_description=design_description,
            measurements=measurements,
            material_preference=material_preference,
            deadline=deadline,
            budget_range=budget_range,
            special_requests=special_requests
        )
        
        # Save reference images
        for image in reference_images:
            order.reference_images.create(image=image)
        
        # Redirect to thank you page
        return redirect('custom_order_thank_you')

 
 
 
 
 
 
 
 
 
 
 

 

class PaymentView(TemplateView):
    template_name = 'checkout.html'


def initiate_payment(request):
    if request.method == 'POST':
        try:
            cart_data = json.loads(request.POST.get('cart_data', '[]'))
            email = request.POST.get('email')
            
            if not email:
                return JsonResponse({
                    'status': False,
                    'message': 'Email is required'
                }, status=400)
            
            # Calculate total amount in kobo
            total_amount = sum(item['price'] * item['quantity'] for item in cart_data) * 100
            
            # Build the absolute callback URL
            callback_url = request.build_absolute_uri(
                reverse('wallflower:verify_payment', kwargs={'reference': 'REFERENCE_PLACEHOLDER'})
            ).replace('REFERENCE_PLACEHOLDER', '{{reference}}')
            
            # Prepare Paystack payload
            payload = {
                'email': email,
                'amount': int(total_amount),
                'currency': 'NGN',
                'callback_url': callback_url,
                'metadata': {
                    'cart_data': cart_data,
                    'customer_id': request.user.id if request.user.is_authenticated else None,
                    'custom_fields': [
                        {
                            'display_name': "Items",
                            'variable_name': "items",
                            'value': f"{len(cart_data)} items"
                        }
                    ]
                }
            }
            
            # Initialize transaction
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            response = requests.post(
                'https://api.paystack.co/transaction/initialize',
                headers=headers,
                data=json.dumps(payload))
            
            if response.status_code == 200:
                data = response.json()
                return JsonResponse({
                    'status': True,
                    'message': 'Payment initialized',
                    'data': data['data']
                })
            
            return JsonResponse({
                'status': False,
                'message': response.json().get('message', 'Payment initialization failed')
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': False,
        'message': 'Invalid request method'
    }, status=400)

def verify_payment(request, reference):
    # Verify Paystack payment
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(
        f'https://api.paystack.co/transaction/verify/{reference}',
        headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] and data['data']['status'] == 'success':
            # Payment successful - process order
            cart_data = data['data']['metadata']['cart_data']
            amount = data['data']['amount'] / 100  # Convert back to Naira
            
            # Process the order (create order records, etc.)
            # ...
            
            # Clear the cart
            if request.user.is_authenticated:
                request.user.cart.all().delete()
            else:
                if 'wallflowerCart' in request.session:
                    del request.session['wallflowerCart']
            
            return render(request, 'payment_success.html', {
                'reference': reference,
                'amount': amount,
                'items': cart_data
            })
    
    # Payment failed
    return render(request, 'payment_failed.html', {
        'reference': reference
    })