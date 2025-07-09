from django.shortcuts import render, redirect
import requests
from django.conf import settings
from django.contrib import messages
from .models import PaymentTransaction
from wallflower.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json

def initiate_payment(request):
    if request.method == 'POST':
        try:
            cart_data = json.loads(request.POST.get('cart_data', '[]'))
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            name = request.POST.get('name')

            if not cart_data:
                messages.error(request, 'Your cart is empty')
                return redirect('wallflower:shop')

            # Get product names for each item in cart
            enriched_cart = []
            total_amount = 0
            for item in cart_data:
                product = Product.objects.get(id=item['id'])
                enriched_item = {
                    'id': item['id'],
                    'name': product.name,
                    'price': float(item['price']),
                    'quantity': item['quantity'],
                    'image': product.image.url if product.image else ''
                }
                enriched_cart.append(enriched_item)
                total_amount += enriched_item['price'] * enriched_item['quantity']

            url = 'https://api.paystack.co/transaction/initialize'
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json',
            }
            data = {
                'email': email,
                'amount': int(total_amount * 100),
                'callback_url': request.build_absolute_uri(reverse('Payment:payment_callback')),
                'metadata': {
                    'address': address,
                    'phone': phone,
                    'cart_data': json.dumps(enriched_cart),
                    'name': name
                }
            }

            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            
            if response.status_code == 200:
                PaymentTransaction.objects.create(
                    email=email,
                    amount=total_amount,
                    reference=response_data['data']['reference'],
                    address=address,
                    phone=phone,
                    name=name,
                    status='initiated',
                    cart_data=enriched_cart
                )
                return redirect(response_data['data']['authorization_url'])
            
            messages.error(request, response_data.get('message', 'Payment initiation failed'))
            return redirect('Payment:payment_fail')
        except Product.DoesNotExist:
            messages.error(request, 'One or more products in your cart no longer exist')
            return redirect('Payment:payment_fail')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('Payment:payment_fail')
    
    return redirect('wallflower:shop')

@csrf_exempt
def payment_callback(request):
    reference = request.GET.get('reference') or request.POST.get('reference')
    
    if reference:
        try:
            verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
            headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
            
            response = requests.get(verify_url, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['data']['status'] == 'success':
                    transaction = PaymentTransaction.objects.get(reference=reference)
                    transaction.status = 'success'
                    transaction.save()
                    
                    # Clear the cart
                    if 'checkoutCart' in request.session:
                        del request.session['checkoutCart']
                    
                    return redirect('Payment:payment_success')
                
        except Exception as e:
            print(f"Callback error: {str(e)}")
    
    return redirect('Payment:payment_fail')

def payment_success(request):
    return render(request, 'Payment/payment_success.html')

def payment_fail(request):
    return render(request, 'Payment/payment_fail.html')
    
    
    
def checkout(request):
    # This view will render the checkout page
    return render(request, 'Payment/checkout.html')
    
    
    
    
    
    
    
