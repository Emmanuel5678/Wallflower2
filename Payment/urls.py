from django.urls import path
from . import views
app_name = 'Payment'
urlpatterns = [
    path('pay/<int:pk>/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
]