"""
from django.urls import path
from . import views
app_name = 'Payment'
urlpatterns = [
    path('pay/<int:pk>/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
]
"""






from django.urls import path
from . import views

app_name = 'Payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-fail/', views.payment_fail, name='payment_fail'),
]