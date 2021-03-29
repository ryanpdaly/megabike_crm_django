from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from apps.common.tests import TestViewBasics
from apps.customers import models


class TestBikeDetailView(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'customers:bike-detail'
		self.url_kwargs = {'pk':10000, 'rn':'TestRahmennummer',}
		self.url_path = 'customers/kd10000/TestRahmennummer/detail/'
		self.template_path = 'customers/bike_detail.html'

		test_user = User.objects.create_user(username=self.username, password=self.password)
		baker.make(models.Customer, kundennummer=10000)
		baker.make(models.Bike, kunde=models.Customer.objects.filter(kundennummer=10000)[0], rahmennummer='TestRahmennummer')

class TestBikeInputView(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'customers:bike-input'
		self.url_kwargs = {'pk':10000}
		self.url_path = 'customers/kd10000/newbike/'
		self.template_path = 'customers/bike_input.html'

		test_user = User.objects.create_user(username=self.username, password=self.password)
		baker.make(models.Customer, kundennummer=10000)

""" This doesn't work, View is also not currently in use
class TestBikeUpdateView(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'customers:bike-update'
		self.url_kwargs = {'kd':10000, 'pk':'TestRahmennummer',}
		self.url_path = 'customers/kd10000/TestRahmennummer/update/'
		self.template_path = 'customers/bike_update.html'

		test_user = User.objects.create_user(username=self.username, password=self.password)
		baker.make(models.Customer, kundennummer=10000)
		baker.make(models.Bike, kunde=models.Customer.objects.filter(kundennummer=10000)[0], rahmennummer='TestRahmennummer')
"""

class TestCustomerDetailView(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'customers:customer-detail'
		self.url_kwargs = {'pk':10000,}
		self.url_path = 'customers/kd10000/detail/'
		self.template_path = 'customers/customer_detail.html'

		test_user1 = User.objects.create_user(username=self.username, password=self.password)

		baker.make(models.Customer, kundennummer=10000)

class TestCustomerInputView(TestViewBasics, TestCase):
	@ classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'customers:customer-input'
		self.url_kwargs = {}
		self.url_path = 'customers/new/'
		self.template_path = 'customers/customer_input.html'

		test_user1 = User.objects.create_user(username=self.username, password=self.password)

class TestCustomerListView(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'customers:customer-list'
		self.url_kwargs = {}
		self.url_path = 'customers/'
		self.template_path = 'customers/customer_list.html'

		# TODO: Test with random number of customers
		num_customers = 15
		pk_start = 10000
		for i in range(num_customers):
			calls = baker.make(models.Customer, pk=(pk_start+i))

		test_user1 = User.objects.create_user(username=self.username, password=self.password)

class TestCustomerUpdateView(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'customers:customer-update'
		self.url_kwargs = {'pk':10000}
		self.url_path = 'customers/kd10000/update/'
		self.template_path = 'customers/customer_update.html'

		test_user1 = User.objects.create_user(username=self.username, password=self.password)
		
		baker.make(models.Customer, kundennummer=10000)