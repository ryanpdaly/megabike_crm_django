from django.contrib import admin
from django.urls import path

from . import views

app_name = 'leasing'
urlpatterns = [
	path('info/<str:unternehmen>/', views.leasing_info_page, name='info-page'),
]