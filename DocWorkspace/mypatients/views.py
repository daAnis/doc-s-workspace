from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import ClinicalRecord, Examination, Temperature, Pressure, Prescription
from .forms import ExaminationForm

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

def examination(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    exam_list = Examination.objects.filter(record=record_id)
    return render(request, 'mypatients/examination.html', {'record': patient, 'examinations': exam_list})

def examination_create(request, ward, record_id):
    data = dict()
    if request.method == 'POST':
        form = ExaminationForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            examinations = Examination.objects.filter(record=record_id)
            data['html_exam_list'] = render_to_string('mypatients/partial_exam_list.html', {
                'examinations': examinations
            })
        else:
            data['form_is_valid'] = False
    else:
        form = ExaminationForm()
    context = {'form': form}
    data['html_form'] = render_to_string('mypatients/partial_exam_create.html',
        context,
        request=request
    )
    return JsonResponse(data)

def observation(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    temp_list = Temperature.objects.filter(record=record_id)
    pres_list = Pressure.objects.filter(record=record_id)
    return render(request, 'mypatients/observation.html', {'record': patient, 'temp': temp_list, 'pressure': pres_list})

def prescription(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    presc_list = Prescription.objects.filter(record=record_id)
    return render(request, 'mypatients/prescription.html', {'record': patient, 'presc': presc_list})