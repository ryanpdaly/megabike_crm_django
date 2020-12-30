from django.contrib import admin
from django.urls import path

from .views import MainView, InputAssona, InputBikeleasing, InputBusinessbike, InputEnra, InputEurorad, InputCombined

app_name = 'insurance'
urlpatterns = [
	path('', MainView.as_view(), name='main'),
	path('input/assona', InputAssona.as_view(), name='input_assona'),
	path('input/bikleasing_service', InputBikeleasing.as_view(), name='input_bikeleasing'),
	path('input/businessbike', InputBusinessbike.as_view(), name='input_businessbike'),
	path('input/enra', InputEnra.as_view(), name='input_enra'),
	path('input/eurorad', InputEurorad.as_view(), name='input_eurorad'),

	path('input', InputCombined.as_view(), name='input_combined')
]