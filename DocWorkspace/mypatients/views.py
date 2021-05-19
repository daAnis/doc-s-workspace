from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import ClinicalRecord, Examination, Temperature, Pressure, Prescription
from .forms import ExaminationForm

def index(request):
    return render(request, "mypatients/index.html", {})


def wards(request):
    records = ClinicalRecord.objects.all()
    wards = set()
    for r in records:
        wards.add(r.ward)
    s_wards = sorted(wards)
    return render(request, "mypatients/wards.html", {"wards": s_wards})


def records_in_ward(request, ward):
    records = ClinicalRecord.objects.filter(ward=ward)
    return render(
        request, "mypatients/patients.html", {"records": records, "ward": ward}
    )


def record(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    return render(request, "mypatients/patient.html", {"record": patient})


def examination(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    exam_list = Examination.objects.filter(record=record_id)
    return render(
        request,
        "mypatients/examination.html",
        {"record": patient, "examinations": exam_list},
    )


def save_examination_form(request, form, record_id, template_name):
    patient = ClinicalRecord.objects.get(pk=record_id)
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            recived_form = form.save(commit=False)
            recived_form.record = patient
            recived_form.save()
            data["form_is_valid"] = True
            examinations = Examination.objects.filter(record=record_id)
            data["html_exam_list"] = render_to_string(
                "mypatients/examination_partials/partial_exam_list.html",
                {
                    "examinations": examinations,
                    "record": patient,
                },
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form, "record": patient}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def examination_create(request, ward, record_id):
    if request.method == "POST":
        form = ExaminationForm(request.POST)
    else:
        form = ExaminationForm()
    return save_examination_form(
        request,
        form,
        record_id,
        "mypatients/examination_partials/partial_exam_create.html",
    )


def examination_update(request, ward, record_id, exam_id):
    exam = Examination.objects.get(pk=exam_id)
    if request.method == "POST":
        form = ExaminationForm(request.POST, instance=exam)
    else:
        form = ExaminationForm(instance=exam)
    return save_examination_form(
        request,
        form,
        record_id,
        "mypatients/examination_partials/partial_exam_update.html",
    )


def examination_delete(request, ward, record_id, exam_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    exam = Examination.objects.get(pk=exam_id)
    data = dict()
    if request.method == "POST":
        exam.delete()
        data["form_is_valid"] = True
        examinations = Examination.objects.filter(record=record_id)
        data["html_exam_list"] = render_to_string(
            "mypatients/examination_partials/partial_exam_list.html",
            {
                "examinations": examinations,
                "record": patient,
            },
        )
    else:
        context = {"record": patient, "examination": exam, }
        data["html_form"] = render_to_string(
            "mypatients/examination_partials/partial_exam_delete.html",
            context,
            request=request,
        )
    return JsonResponse(data)


def observation(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    temp_list = Temperature.objects.filter(record=record_id)
    pres_list = Pressure.objects.filter(record=record_id)
    return render(
        request,
        "mypatients/observation.html",
        {"record": patient, "temp": temp_list, "pressure": pres_list},
    )


def prescription(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    presc_list = Prescription.objects.filter(record=record_id)
    return render(
        request,
        "mypatients/prescription.html",
        {"record": patient, "presc": presc_list},
    )
