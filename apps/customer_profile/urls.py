from django.contrib import admin
from django.urls import path, reverse

from . import views

app_name='customers'
urlpatterns = [
	#path('', MainView.as_view(), name='main'),
	path('', views.CustomerListView.as_view(), name='customer-list'),
	path('view/<int:pk>/', views.CustomerDetailView, name='customer-detail'),
	path('input/customer/', views.InputCustomer.as_view(), name='input-customer'),
	path('input/fahrzeug/', views.InputFahrzeug.as_view(), name='input_fahrzeug'),
]