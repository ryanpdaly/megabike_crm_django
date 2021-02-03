from django.contrib import admin
from django.urls import path, reverse

from . import views

app_name='customers'
urlpatterns = [
	#path('', MainView.as_view(), name='main'),
	path('', views.CustomerListView.as_view(), name='customer-list'),
	path('newcustomer', views.InputCustomer.as_view(), name='customer-input'),
	path('kd<int:pk>/', views.CustomerDetailView, name='customer-detail'),
	path('kd<int:pk>/newbike/', views.InputBikeView, name='bike-input'),
	path('kd<int:pk>/<str:rn>/', views.BikeDetailView, name='bike-detail')
]