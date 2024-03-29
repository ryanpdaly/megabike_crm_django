"""megabike_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.urls import reverse, reverse_lazy

from . import settings

urlpatterns = [
    path('', RedirectView.as_view(url='customers/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),    
    path('admin/', admin.site.urls),

    path('common/', include('apps.common.urls')),
    path('contact/', include('apps.contact.urls')),
    #path('contact/', RedirectView.as_view(url=reverse_lazy('call-list', kwargs={'abteilung':'all', 'filter':'all'}), permanent=False)),
    path('customers/', include('apps.customers.urls')),
    path('insurance/', include('apps.insurance.urls')),
    path('leasing/', include('apps.leasing.urls')),
    path('warranty/', include('apps.warranty.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)