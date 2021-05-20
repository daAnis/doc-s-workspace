from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from datetime import date

from .models import ClinicalRecord, Examination, Temperature, Pressure, Prescription
from .forms import ExaminationForm, PrescriptionForm, PressureForm

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

def save_bpp_form(request, form, record_id, template_name):
    patient = ClinicalRecord.objects.get(pk=record_id)
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            recived_form = form.save(commit=False)
            recived_form.record = patient
            recived_form.save()
            data["form_is_valid"] = True
            bpps = Pressure.objects.filter(record=record_id)
            data["html_bpp_list"] = render_to_string(
                "mypatients/observation_partials/partial_bpp_list.html",
                {
                    "bpps": bpps,
                    "record": patient,
                },
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form, "record": patient}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def bpp_create(request, ward, record_id):
    if request.method == "POST":
        form = PressureForm(request.POST)
    else:
        form = PressureForm()
    return save_bpp_form(
        request,
        form,
        record_id,
        "mypatients/observation_partials/partial_bpp_create.html",
    )


def bpp_update(request, ward, record_id, bpp_id):
    bpp = Pressure.objects.get(pk=bpp_id)
    if request.method == "POST":
        form = PressureForm(request.POST, instance=bpp)
    else:
        form = PressureForm(instance=bpp)
    return save_bpp_form(
        request,
        form,
        record_id,
        "mypatients/observation_partials/partial_bpp_update.html",
    )


def bpp_delete(request, ward, record_id, bpp_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    bpp = Pressure.objects.get(pk=bpp_id)
    data = dict()
    if request.method == "POST":
        bpp.delete()
        data["form_is_valid"] = True
        bpps = Pressure.objects.filter(record=record_id)
        data["html_bpp_list"] = render_to_string(
            "mypatients/observation_partials/partial_bpp_list.html",
            {
                "bpps": bpps,
                "record": patient,
            },
        )
    else:
        context = {"record": patient, "bpp": bpp, }
        data["html_form"] = render_to_string(
            "mypatients/observation_partials/partial_bpp_delete.html",
            context,
            request=request,
        )
    return JsonResponse(data)

def prescription(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    presc_list = Prescription.objects.filter(record=record_id)
    return render(
        request,
        "mypatients/prescription.html",
        {"record": patient, "prescriptions": presc_list},
    )

def save_prescription_form(request, form, record_id, template_name):
    patient = ClinicalRecord.objects.get(pk=record_id)
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            recived_form = form.save(commit=False)
            recived_form.record = patient
            recived_form.save()
            data["form_is_valid"] = True
            prescriptions = Prescription.objects.filter(record=record_id)
            data["html_pr_list"] = render_to_string(
                "mypatients/prescription_partials/partial_pr_list.html",
                {
                    "prescriptions": prescriptions,
                    "record": patient,
                },
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form, "record": patient}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def prescription_create(request, ward, record_id):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
    else:
        form = PrescriptionForm()
    return save_prescription_form(
        request,
        form,
        record_id,
        "mypatients/prescription_partials/partial_pr_create.html",
    )


def prescription_update(request, ward, record_id, pr_id):
    pr = Prescription.objects.get(pk=pr_id)
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=pr)
    else:
        form = PrescriptionForm(instance=pr)
    return save_prescription_form(
        request,
        form,
        record_id,
        "mypatients/prescription_partials/partial_pr_update.html",
    )


def prescription_delete(request, ward, record_id, pr_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    pr = Prescription.objects.get(pk=pr_id)
    data = dict()
    if request.method == "POST":
        if pr.date_1 <= date.today():
            pr.date_2 = date.today()
            pr.save()
        else:
            pr.delete()
        data["form_is_valid"] = True
        prescriptions = Prescription.objects.filter(record=record_id)
        data["html_pr_list"] = render_to_string(
            "mypatients/prescription_partials/partial_pr_list.html",
            {
                "prescriptions": prescriptions,
                "record": patient,
            },
        )
    else:
        context = {"record": patient, "prescription": pr, }
        data["html_form"] = render_to_string(
            "mypatients/prescription_partials/partial_pr_delete.html",
            context,
            request=request,
        )
    return JsonResponse(data)