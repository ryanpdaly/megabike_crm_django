from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse


class IndexView(TemplateView):
	template_name = 'common/base.html'


class MainView(TemplateView):
	template_name = 'common/main.html'


def privacy_policy(request):
	return render(request, 'common/privacy_policy.html')


def error_404(request):
	data = {}
	return render(request, 'common/error_404.html', data)
	