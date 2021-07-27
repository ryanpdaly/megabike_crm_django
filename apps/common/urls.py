from django.urls import path

from apps.common import views


app_name = 'common'
urlpatterns = [
    path('', views.MainView.as_view(), name='main-redirect'),
    path('main/', views.MainView.as_view(), name='main'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('privacy/', views.privacy_policy, name='privacy-policy'),
]