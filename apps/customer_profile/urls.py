from django.contrib import admin
from django.urls import path

from .views import MainView, InputCustomer, InputFahrzeug

app_name='customers'
urlpatterns = [
	path('', MainView.as_view(), name='main'),
	path('input/customer', InputCustomer.as_view(), name='input_customer'),
	path('input/fahrzeug', InputFahrzeug.as_view(), name='input_fahrzeug')
]