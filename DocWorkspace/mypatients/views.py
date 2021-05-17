from django.shortcuts import render

from .models import ClinicalRecord

# Create your views here.
def index(request):
    return render(request, 'mypatients/index.html', {})

def wards(request):
    records = ClinicalRecord.objects.all()
    wards = set()
    for r in records:
        wards.add(r.ward)
    s_wards = sorted(wards)
    return render(request, 'mypatients/wards.html', {'wards': s_wards})

def records_in_ward(request, ward):
    records = ClinicalRecord.objects.filter(ward=ward)
    return render(request, 'mypatients/patients.html', {'records': records, 'ward': ward})

def record(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    return render(request, 'mypatients/patient.html', {'record': patient})