from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from apps.common import mixins as common_mixins

# TODO: Rework as CBV
@login_required
def leasing_info_page(request, unternehmen):
	"""
	Function based view used to display basic, general information for leasing companies
	"""

	context = {
		'open_contact_tickets': common_mixins.get_user_contact_tickets(request),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(request),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(request),
	}

	return render(request, f'leasing/info_{unternehmen}.html', context=context)