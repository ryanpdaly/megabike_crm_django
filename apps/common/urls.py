from django.urls import path

from ..common.views import IndexView, LoginView

app_name = 'common'
urlpatterns = [
    path('index/', IndexView.as_view()),
    path('', LoginView.as_view()),

]