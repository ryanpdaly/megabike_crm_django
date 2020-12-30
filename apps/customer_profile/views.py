from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from .models import CustomerProfile, FahrzeugProfile
from .forms import CustomerForm, FahrzeugForm

# Create your views here.
class MainView(TemplateView):
	template_name = 'customers/main.html'

class InputCustomer(CreateView):
	model = CustomerProfile
	form_class = CustomerForm
	template_name = 'customers/profile.html'

class InputFahrzeug(CreateView):
	model = FahrzeugProfile
	form_class = FahrzeugForm
	template_name = 'customers/fahrzeug.html'