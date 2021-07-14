from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse

class IndexView(TemplateView):
	template_name = 'common/base.html'
'''
class LoginView(TemplateView):
	template_name = 'common/login.html'
'''

class MainView(TemplateView):
	template_name = 'common/main.html'

def privacy_policy(request):
	return render(request, 'common/privacy_policy.html')

	