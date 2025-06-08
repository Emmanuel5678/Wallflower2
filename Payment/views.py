

# Create your views here.



from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.conf import settings
from django.contrib import messages
from .models import PaymentTransaction
from wallflower.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse

def initiate_payment(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        amount_str = request.POST.get('amount')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        name = request.POST.get('name')

        # Validate amount
        if not amount_str:
            messages.error(request, 'Amount is required')
            return render(request, 'Payment/payment_form.html', {'product': product})
        
        try:
            amount = float(amount_str)
        except ValueError:
            messages.error(request, 'Invalid amount format')
            return render(request, 'Payment/payment_form.html', {'product': product})

        if amount <= 0:
            messages.error(request, 'Amount must be positive')
            return render(request, 'Payment/payment_form.html', {'product': product})

        # Paystack API endpoint
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': email,
            'amount': int(amount * 100),  # Convert to kobo
            'callback_url': request.build_absolute_uri(reverse('Payment:payment_callback')),
            'metadata': {
                'address': address,
                'phone': phone,
                'product_id': product.id,
                'name' : name # Include product ID in metadata
            }
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            authorization_url = response_data['data']['authorization_url']
            reference = response_data['data']['reference']

            PaymentTransaction.objects.create(
                email=email,
                amount=amount,
                reference=reference,
                address=address,
                phone=phone,
                product=product,
                name = name,
                status='initiated'
            )

            return redirect(authorization_url)
        else:
            error_message = response.json().get('message', 'Payment initiation failed')
            return render(request, 'Payment/error.html', {'message': error_message})
    
    # GET request - show payment form
    return render(request, 'Payment/payment_form.html', {
        'product': product,
        'default_amount': product.price, 
        'default_name' : product.name# Pre-fill with product price
    })
    
    
    
    
    
    
    


@csrf_exempt
def payment_callback(request):
    # Get reference from either GET or POST
    reference = request.GET.get('reference') or request.POST.get('reference')
    
    if reference:
        # Verify with Paystack
        verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
        headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
        
        try:
            response = requests.get(verify_url, headers=headers)
            if response.status_code == 200 and response.json()['data']['status'] == 'success':
                # Update transaction status
                transaction = PaymentTransaction.objects.get(reference=reference)
                transaction.status = 'success'
                transaction.save()
                
                # Redirect to shop with success message
                return redirect(reverse('wallflower:shop') + '?payment=success')
        except Exception:
            pass
    
    # If anything fails, redirect back with error
    return redirect(reverse('wallflower:shop') + '?payment=error')