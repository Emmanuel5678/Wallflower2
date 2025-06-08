from django.urls import path,include
from . import views
from .views import initiate_payment, verify_payment
from django.conf.urls.static import static
from django.conf import settings


app_name = 'wallflower'


urlpatterns = [
     path('', views.home, name='home'),
     path('about/', views.about, name='about'),
     path('services/', views.services, name='services'),
     path('contact/', views.contact, name='contact'),
     path('gallery/', views.gallery, name='gallery'),
     path('custom_order/', views.custom_order, name='custom_order'),
     path('shop/', views.shop, name='shop'),
     path('login/', views.login_user, name='login'),
     path('logout/', views.logout_user, name='logout'),
     path('signup/', views.signup, name='signup'),
     path('initiate/',views.initiate_payment, name='initiate_payment'),
        path('verify/<str:reference>/',views.verify_payment, name='verify_payment'),
        
        
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)