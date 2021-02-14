from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
@login_required
def leasing_info_page(request, unternehmen):
	return render(request, f'leasing/info_{unternehmen}.html')