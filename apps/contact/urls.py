from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.urls import reverse, reverse_lazy

from apps.contact import views


app_name = 'contact'
urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('contact:call-list', kwargs={'abteilung':'all', 'filter':'all'}), permanent=True)),
	re_path(r'^anfrage/list/abteilung=(?P<abteilung>\w+)/filter=(?P<filter>\w+)$', views.CallList.as_view(), name='call-list'),
	path('anfrage/new/', views.CreatePhoneContact.as_view(), name='call-create'),
	path('anfrage/<int:pk>/update_status/', views.UpdatePhoneContactStatus.as_view(), name='call-update-status'),

	path('ausgehend/list/', views.OutgoingCallList.as_view(), name='outgoing-list'),
	path('ausgehend/new/', views.OutgoingCallCreate.as_view(), name='outgoing-create'),
	path('ausgehend/<int:pk>/update/', views.OutgoingCallUpdate.as_view(), name='outgoing-update')
]