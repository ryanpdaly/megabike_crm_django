from django.contrib import admin
from django.urls import path

from apps.insurance import views

app_name = 'orders'
urlpatterns = [
	path('input_<str:insurance>/<str:rn>/', views.input_insurance, name='input-insurance'),
	path('view/all/', views.list_all, name='list-all'),
	path('info/<str:insurance>/', views.info_page, name='info-page'),
	path('display/<str:rn>/', views.display_policy, name='display-policy'),
]