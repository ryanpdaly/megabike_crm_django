from django.contrib import admin
from django.urls import path, reverse

from apps.customers import views

app_name='customers'
urlpatterns = [
	#path('', MainView.as_view(), name='main'),
	path('kd<int:pk>/detail/', views.customer_detail_view, name='customer-detail'),	
	path('new/', views.CustomerInputView.as_view(), name='customer-input'),	
	path('', views.CustomerListView.as_view(), name='customer-list'),
	path('kd<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer-update'),

	path('kd<int:pk>/<str:rn>/detail/', views.bike_detail_view, name='bike-detail'),
	path('kd<int:pk>/newbike/', views.bike_input_view, name='bike-input'),
	# TODO: Inconsistent - Why does this not use pk for kundennummer, rn for rahmennummer?
	path('kd<int:kd>/<str:pk>/update/', views.BikeUpdateView.as_view(), name='bike-update'),
]