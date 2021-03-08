from django.contrib import admin
from django.urls import path

from . import views

app_name = 'contact'
urlpatterns = [
	path('', views.CallList.as_view(), name='call-list'),
	path('add/', views.CreatePhoneContact.as_view(), name='create-call'),
	path('update_status/<int:pk>/', views.UpdatePhoneContactStatus.as_view(), name='call-status-update'),
]