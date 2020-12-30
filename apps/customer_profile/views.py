from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from django.forms.models import inlineformset_factory

from .models import CustomerProfile, FahrzeugProfile
from .forms import CustomerForm, FahrzeugForm

ChildFormset = inlineformset_factory(
	CustomerProfile, FahrzeugProfile, fields='__all__', extra=1
	)

# Create your views here.
class MainView(TemplateView):
	template_name = 'customer_profile/main.html'

class CustomerListView(ListView):
	model = CustomerProfile

class InputCustomer(CreateView):
	model = CustomerProfile
	#form_class = CustomerForm
	template_name = 'customer_profile/input_customer.html'
	fields = ['kundennummer']

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		if self.request.POST:
			data['children'] = ChildFormset(self.request.POST)
		else:
			data['children'] = ChildFormset()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		children = context['children']
		self.object = form.save()
		if children.is_valid():
			children.instance = self.object
			children.save()
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('parents:list')

class InputFahrzeug(CreateView):
	model = FahrzeugProfile
	form_class = FahrzeugForm
	template_name = 'customer_profile/fahrzeug.html'