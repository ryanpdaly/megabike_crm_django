from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from .models import AssonaInfo, BikeleasingInfo, BusinessbikeInfo, EnraInfo, EuroradInfo
from .forms import AssonaForm, BikeleasingForm, BusinessbikeForm, EnraForm, EuroradForm

def index(request):
	return HttpResponse('Hello from Django!')

class MainView(TemplateView):
	template_name = 'insurance/main.html'

class InputAssona(CreateView):
	model = AssonaInfo
	form_class = AssonaForm
	template_name = 'insurance/input_assona.html'

class InputBikeleasing(CreateView):
	model = BikeleasingInfo
	form_class = BikeleasingForm
	template_name = 'insurance/input_bikeleasing.html'

class InputBusinessbike(CreateView):
	model = BusinessbikeInfo
	form_class = BusinessbikeForm
	template_name = 'insurance/input_businessbike.html'

class InputEnra(CreateView):
	model = EnraInfo
	form_class = EnraForm
	template_name = 'insurance/input_enra.html'

class InputEurorad(CreateView):
	model = EuroradInfo
	form_class = EuroradForm
	template_name = 'insurance/input_eurorad.html'

class InputCombined(TemplateView):
	template_name = 'insurance/input_combined.html'