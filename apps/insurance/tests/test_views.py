from http import HTTPStatus

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from apps.common.tests import TestViewBasics
from apps.insurance import models
from apps.customers import models as customer_models


class TestInputInsurance(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		#Creates user
		super().setUpTestData()

		self.url_name = 'insurance:input-insurance'
		self.url_kwargs = {'insurance':'as', 'rn':'TestRahmennummer',}
		self.url_path = 'insurance/input_as/TestRahmennummer/'
		self.template_path = 'insurance/input_insurance.html'

		baker.make(customer_models.Customer, kundennummer=10000)
		baker.make(customer_models.Bike, kunde=customer_models.Customer.objects.filter(kundennummer=10000)[0], 
					rahmennummer='TestRahmennummer'
				)

class TestListAll(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		#Creates user
		super().setUpTestData()

		self.url_name = 'insurance:list-all'
		self.url_kwargs = {}
		self.url_path = 'insurance/view/all/'
		self.template_path = 'insurance/list_all.html'

class TestInfoPage(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		#Creates user
		super().setUpTestData()

		self.url_name = 'insurance:info-page'
		self.url_kwargs = {'insurance':'assona'}
		self.url_path = 'insurance/info/assona/'
		self.template_path = 'insurance/info_assona.html'

class TestDisplayPolicy(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		#Creates user
		super().setUpTestData()

		self.url_name = 'insurance:display-policy'
		self.url_kwargs = {'rn':'TestRahmennummer',}
		self.url_path = 'insurance/display/TestRahmennummer/'
		self.template_path = 'insurance/display_assona.html'

		baker.make(customer_models.Customer, kundennummer=10000)
		baker.make(customer_models.Bike, kunde=customer_models.Customer.objects.filter(kundennummer=10000)[0], 
					rahmennummer='TestRahmennummer', insurance='as'
				)
		baker.make(models.AssonaInfo, rahmennummer=customer_models.Bike.objects.filter(rahmennummer='TestRahmennummer')[0])