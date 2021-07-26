from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from mypatients.models import Patient, ClinicalRecord

@login_required
def index(request):
    return render(request, "emergencydocapp/index.html")

@login_required
def create_new_patient(request):
    pass

@login_required
def search_patient(request):
    query_for_search = request.POST.get('search_field')
    print(query_for_search)
    data = dict()
    context = { 'records': Patient.objects.filter(name__icontains=query_for_search) }
    data['html_patients'] = render_to_string('emergencydocapp/search_results.html', context)
    return JsonResponse(data)