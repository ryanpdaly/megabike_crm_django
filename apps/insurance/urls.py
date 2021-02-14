from django.contrib import admin
from django.urls import path

from . import views

app_name = 'insurance'
urlpatterns = [
	path('input_<str:insurance>/<str:rn>/', views.input_insurance, name='input-insurance'),
	path('view_all/', views.list_all, name='list-all'),
	path('info_<str:insurance>/', views.info_page, name='info-page')
]