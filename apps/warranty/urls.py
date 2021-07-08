from django.contrib import admin
from django.urls import path, re_path

from apps.warranty import views

app_name = 'warranty'
urlpatterns = [
	path('', views.TicketList.as_view(), name='main'),
	path('new/', views.CreateTicket.as_view(), name='new-ticket'),
	re_path(r'^new/(?P<kdnr_input>[0-9]?)(?P<kdnr_checked>[0-9]?)', views.CreateTicket.as_view(), name='new-ticket'),
	path('display<int:pk>/', views.DisplayTicket.as_view(), name='display-ticket'),
	#path('edit<int:pk>/', views.UpdateTicket.as_view(), name='update-ticket'),
	path('edit<int:pk>/', views.UpdateTicket.as_view(), name='update-ticket'),
	path('addfile<int:pk>/', views.AddFile.as_view(), name='add-file'),
	path('update<int:pk>/', views.UpdateStatus.as_view(), name='update-status'),
	path('display<int:pk>/file<int:sk>', views.display_file, name='display-file')
]