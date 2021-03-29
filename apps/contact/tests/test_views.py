from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from apps.contact import models
from apps.common.tests import TestViewBasics


class TestCallList(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'contact:call-list'
		self.url_kwargs = {}
		self.url_path = 'contact/'
		self.template_path = 'contact/phonecontact_list.html'

		calls = baker.make(models.PhoneContact, _quantity=15)

		test_user1 = User.objects.create_user(username='testuser1', password='TestPassword')

class TestCreatePhoneContact(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'contact:call-create'
		self.url_kwargs = {}
		self.url_path = 'contact/new/'
		self.template_path = 'contact/phonecontact_create.html'

		test_user1 = User.objects.create_user(username='testuser1', password='TestPassword')

class TestUpdatePhoneContactStatus(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		self.username = 'testuser1'
		self.password = 'TestPassword'

		self.url_name = 'contact:call-update-status'
		self.url_kwargs = {'pk':1}
		self.url_path = 'contact/update_status/1/'
		self.template_path = 'contact/phonecontact_update_status.html'

		baker.make(models.PhoneContact, id=1)

		test_user1 = User.objects.create_user(username='testuser1', password='TestPassword')
