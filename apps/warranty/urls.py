from django.contrib import admin
from django.urls import path

from . import views

app_name = 'warranty'
urlpatterns = [
	path('', views.TicketList.as_view(), name='main'),
	path('new', views.CreateTicket.as_view(), name='new-ticket'),
	path('display<int:pk>', views.DisplayTicket.as_view(), name='display-ticket'),
	path('edit<int:pk>', views.UpdateTicket.as_view(), name='update-ticket'),
]