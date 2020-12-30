
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
	template_name = 'common/base.html'

class LoginView(TemplateView):
	template_name = 'common/login.html'