from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse


class IndexView(TemplateView):
	"""
	A class based view for our base template
	"""

	template_name = 'common/base.html'

class MainView(TemplateView):
	"""
	A class based view for our main landing screen. Not currently in use.
	"""

	template_name = 'common/main.html'

def privacy_policy(request):
	"""
	A function based view to display our privacy policy
	"""
	return render(request, 'common/privacy_policy.html')
