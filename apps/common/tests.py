from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class TestViewBasics(object):

	def test_redirect_if_not_logged_in(self):
		response = self.client.get(reverse(self.url_name, kwargs=self.url_kwargs))
		self.assertRedirects(response, f'/accounts/login/?next=/{self.url_path}')

	def test_view_url_exists(self):
		login = self.client.login(username=self.username, password=self.password)

		response = self.client.get('/' + self.url_path)
		self.assertEqual(response.status_code, 200)

	def test_view_accessible_by_name(self):
		login = self.client.login(username=self.username, password=self.password)

		response = self.client.get(reverse(self.url_name, kwargs=self.url_kwargs))
		self.assertEqual(response.status_code, 200)

	def test_view_uses_correct_template(self):
		login = self.client.login(username=self.username, password=self.password)

		response = self.client.get(reverse(self.url_name, kwargs=self.url_kwargs))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, self.template_path)