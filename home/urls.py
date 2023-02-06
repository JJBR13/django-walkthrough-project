from django.shortcuts import render
from django.urls import path
from . import views

# Create your views here.


urlpatterns = [
    path('', views.index, name='home')
]
