from django.contrib import admin
from django.urls import path

from . import views

app_name = 'insurance'
urlpatterns = [
	path('', views.MainView.as_view(), name='main'),
	path('input_assona/<str:rn>', views.assona_input_view, name='input-assona'),
	path('input_<str:insurance>/<str:rn>', views.input_insurance, name='input-insurance'),
]