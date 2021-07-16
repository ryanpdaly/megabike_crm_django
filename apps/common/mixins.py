
# A mixin to pass required context data to our class based views in order to show alerts
class AlertsMixin:
	def get_context_data(self, request, *args, **kwargs):
		data = super().get_context_data(request, *args, **kwargs)

		# Custom context data goes here

		return data

class CustomerSearchMixin:
	def get_context_data(self, request, *args, **kwargs):
		data = super().get_context_data(request, *args, **kwargs)

		# Custom context data goes here

		return data