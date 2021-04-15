from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.urls import reverse, reverse_lazy

from apps.contact import views


app_name = 'contact'
# TODO: These url names/patterns are not consistent
urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('contact:call-list', kwargs={'abteilung':'all', 'filter':'all'}), permanent=True)),
	re_path(r'^(?P<abteilung>\w+)/(?P<filter>\w+)$', views.CallList.as_view(), name='call-list'),
	path('new/', views.CreatePhoneContact.as_view(), name='call-create'),
	path('update_status/<int:pk>/', views.UpdatePhoneContactStatus.as_view(), name='call-update-status'),
]