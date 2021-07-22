from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from apps.common import mixins as common_mixins

# TODO: Rework as CBV
@login_required
def leasing_info_page(request, unternehmen):

	context = {
		'open_contact_tickets': common_mixins.get_open_contact_tickets(),
		'faellige_insurance_tickets': common_mixins.get_faellige_insurance_tickets(),
		'faellige_warranty_tickets': common_mixins.get_faellige_warranty_tickets(),
	}

	return render(request, f'leasing/info_{unternehmen}.html', context=context)