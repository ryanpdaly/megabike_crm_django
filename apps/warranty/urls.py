from django.contrib import admin
from django.urls import path, re_path

from apps.warranty import views

app_name = 'warranty'
urlpatterns = [
	path('', views.TicketList.as_view(), name='main'),
	
	# TODO: Flip URL-names? new-ticket --> ticket-new
	path('new/', views.CreateTicket.as_view(), name='new-ticket'),
	re_path(r'^new(?P<kdnr_input>[0-9]?)(?P<kdnr_checked>[0-9]?)', views.CreateTicket.as_view(), name='new-ticket'),
	
	path('<int:pk>/display/', views.DisplayTicket.as_view(), name='display-ticket'),
	path('<int:pk>/edit/', views.UpdateTicket.as_view(), name='update-ticket'),
	path('<int:pk>/addfile/', views.AddFile.as_view(), name='add-file'),
	path('<int:pk>/update/', views.UpdateStatus.as_view(), name='update-status'),
	path('<int:pk>/displayfile<int:sk>', views.display_file, name='display-file')
]