from django.contrib import admin
from django.urls import path, re_path

from apps.insurance import views

app_name = 'insurance'
urlpatterns = [
	# These URLs do not have a consistent pattern
	path('input_<str:insurance>/<str:rn>/', views.input_insurance, name='input-insurance'),
	path('police/all/', views.list_all, name='list-all'),
	path('police/<str:rn>/', views.display_policy, name='display-policy'),	
	path('info/<str:insurance>/', views.info_page, name='info-page'),

	re_path(r'^schaden/list=(?P<filter>\w+)$', views.schaden_list, name='schaden-list'),
	
	# Can't add trailing / to this without getting an error
	path('schaden/new', views.SchadenCreate.as_view(), name='schaden-new'),
	re_path(r'^schaden/new(?P<kdnr_input>[0_9]?)(?P<kdnr_checked>[0-9]?)', views.SchadenCreate.as_view(), name='schaden-new'),
	
	path('schaden<str:pk>/details', views.SchadenDetail.as_view(), name='schaden-detail'),
	path('schaden<str:pk>/details/modal', views.SchadenDetailModal.as_view(), name='schaden-detail-modal'),
	
	path('schaden<int:pk>/edit/', views.SchadenEdit.as_view(), name='schaden-edit'),
	#path('schaden<int:pk>/edit/', views.SchadenEditModal.as_view(), name='schaden-edit-modal'),
	path('schaden<int:pk>/status/', views.SchadenStatusUpdate.as_view(), name='schaden-status'),
	path('schaden<int:pk>/addfile/', views.SchadensmeldungAddFile.as_view(), name='schaden-file-add'),
	path('schaden<int:pk>/viewfile<int:sk>', views.display_file, name='schaden-file-display'),
]