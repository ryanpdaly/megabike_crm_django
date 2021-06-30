from django.contrib import admin
from django.urls import path

from apps.insurance import views

app_name = 'insurance'
urlpatterns = [
	# These URLs do not have a consistent pattern
	path('input_<str:insurance>/<str:rn>/', views.input_insurance, name='input-insurance'),
	path('police/all/', views.list_all, name='list-all'),
	path('police/<str:rn>/', views.display_policy, name='display-policy'),	
	path('info/<str:insurance>/', views.info_page, name='info-page'),

	path('schaden/all/', views.schaden_list, name='schaden-list'),
	path('schaden/<str:pk>/', views.SchadenDetail.as_view(), name='schaden-detail'),
	path('schaden/new/', views.SchadenCreate.as_view(), name='schaden-new'),
	path('schaden/<int:pk>/edit/', views.SchadenEdit.as_view(), name='schaden-edit'),
	path('schaden/<int:pk>/status/', views.SchadenStatusUpdate.as_view(), name='schaden-status'),
]