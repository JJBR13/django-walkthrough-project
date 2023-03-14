from django.urls import path
from . import views

# Create your views here.


urlpatterns = [
    path('', views.checkout, name='checkout'),
    # /<''> passing in an argument
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
]
