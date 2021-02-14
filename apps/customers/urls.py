from django.contrib import admin
from django.urls import path, reverse

from . import views

app_name='customers'
urlpatterns = [
	#path('', MainView.as_view(), name='main'),
	path('', views.CustomerListView.as_view(), name='customer-list'),
	path('newcustomer', views.CustomerInputView.as_view(), name='customer-input'),
	path('details/kd<int:pk>/', views.CustomerDetailView, name='customer-detail'),
	path('edit/kd<int:pk>/', views.CustomerUpdateView.as_view(), name='customer-update'),

	path('kd<int:pk>/newbike/', views.bike_input_view, name='bike-input'),
	path('kd<int:pk>/<str:rn>/detail', views.BikeDetailView, name='bike-detail'),
	path('kd<int:kd>/<str:pk>/edit', views.BikeUpdateView.as_view(), name='bike-update'),
]