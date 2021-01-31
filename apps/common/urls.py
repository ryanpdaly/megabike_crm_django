from django.urls import path

from . import views

app_name = 'common'
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('privacy/', views.privacy_policy, name='privacy-policy'),
]