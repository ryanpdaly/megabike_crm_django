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
		super().setUpTestData()

		self.url_name = 'contact:call-list'
		self.url_kwargs = {'abteilung':'all', 'filter':'all'}
		self.url_path = 'contact/all/all'
		self.template_path = 'contact/phonecontact_list.html'

		calls = baker.make(models.PhoneContact, _quantity=15)

	# Need to test our custom get_queryset

class TestCreatePhoneContact(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		super().setUpTestData()

		self.url_name = 'contact:call-create'
		self.url_kwargs = {}
		self.url_path = 'contact/new/'
		self.template_path = 'contact/phonecontact_create.html'

class TestUpdatePhoneContactStatus(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		super().setUpTestData()

		self.url_name = 'contact:call-update-status'
		self.url_kwargs = {'pk':1}
		self.url_path = 'contact/update_status/1/'
		self.template_path = 'contact/phonecontact_update_status.html'

		baker.make(models.PhoneContact, id=1)

	# Need to test our customer get_context_data

class TestOutgoingCallList(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		super().setUpTestData()

		self.url_name = 'contact:outgoing-list'
		self.url_kwargs = {}
		self.url_path = 'contact/ausgehend/'
		self.template_path = 'contact/outgoingcall_list.html'

		baker.make(models.OutgoingCall)

	# Need to test our custom get_queryset

class TestOutgoingCallCreate(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		super().setUpTestData()

		self.url_name = 'contact:outgoing-create'
		self.url_kwargs = {}
		self.url_path = 'contact/ausgehend/new/'
		self.template_path = 'contact/outgoingcall_create.html'

class TestOutgoingCallUpdate(TestViewBasics, TestCase):
	@classmethod
	def setUpTestData(self):
		super().setUpTestData()

		self.url_name = 'contact:outgoing-update'
		self.url_kwargs = {'pk':1}
		self.url_path = 'contact/ausgehend/update/1/'
		self.template_path = 'contact/outgoingcall_update.html'

		baker.make(models.OutgoingCall, id=1)
	# Need to test custom get_context_data