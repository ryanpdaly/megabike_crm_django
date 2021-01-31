from django.db import models
from django.urls import reverse, reverse_lazy

class Customer(models.Model):
	kundennummer = models.IntegerField(unique=True, primary_key=True)
	nachname = models.CharField(max_length=30)

	class Meta:
		verbose_name = "Customer"
		verbose_name_plural = "Customers"

	def __str__(self):
		return self.nachname

	def get_absolute_url(self):
		return reverse('customers:customer-detail', args=[str(self.kundennummer)])

class Bike(models.Model):
	kundennummer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	
	beschreibung = models.CharField(max_length=50)
	rahmennummer = models.CharField(max_length=30)

	INSURANCE_OPTIONS = (
		('no', 'None'),
		('as', 'Assona'),
		('bu', 'Businessbike'),
		('bl', 'Bikeleasing Service'),
		('en', 'ENRA'),
		('eu', 'Eurorad'),
	)

	insurance = models.CharField(
		max_length = 2,
		choices = INSURANCE_OPTIONS,
		blank = False,
		default = 'no',
		help_text = 'Versicherungsunternehmen')

	class Meta:
		verbose_name = "Bike"
		verbose_name_plural = "Bikes"

	def __str__(self):
		return self.beschreibung

	def get_absolute_url(self):
		return reverse_lazy('customers:bike-detail', args=[str(self.id)])
