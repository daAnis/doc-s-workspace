from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from datetime import date, datetime, timezone

from .models import ClinicalRecord, Examination, Temperature, Pressure, Prescription
from .forms import ExaminationForm, PrescriptionForm, PressureForm, TemperatureForm


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
        context = {
            "record": patient,
            "examination": exam,
        }
        data["html_form"] = render_to_string(
            "mypatients/examination_partials/partial_exam_delete.html",
            context,
            request=request,
        )
    return JsonResponse(data)


def observation(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    temps = Temperature.objects.filter(record=record_id)
    bpps = Pressure.objects.filter(record=record_id)
    return render(
        request,
        "mypatients/observation.html",
        {"record": patient, "temps": temps, "bpps": bpps},
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
        context = {
            "record": patient,
            "bpp": bpp,
        }
        data["html_form"] = render_to_string(
            "mypatients/observation_partials/partial_bpp_delete.html",
            context,
            request=request,
        )
    return JsonResponse(data)


def temp_get(request, ward, record_id):
    labels = []
    data = []
    temps = Temperature.objects.filter(record=record_id)
    for t in temps:
        labels.append(t.date_time)
        data.append(t.value)
    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


def save_temp_form(request, form, record_id, template_name):
    patient = ClinicalRecord.objects.get(pk=record_id)
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            recived_form = form.save(commit=False)
            recived_form.record = patient
            recived_form.save()
            data["form_is_valid"] = True
            temps = Temperature.objects.filter(record=record_id)
        else:
            data["form_is_valid"] = False
    context = {"form": form, "record": patient}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def temp_create(request, ward, record_id):
    if request.method == "POST":
        form = TemperatureForm(request.POST)
    else:
        form = TemperatureForm()
    return save_temp_form(
        request,
        form,
        record_id,
        "mypatients/observation_partials/partial_temp_create.html",
    )


def temp_update(request, ward, record_id, temp_label):
    date = datetime.strptime(temp_label, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc
    )
    temps = Temperature.objects.filter(record=record_id)
    temp = Temperature.objects.first()
    for t in temps:
        if (
            date.year == t.date_time.year
            and date.month == t.date_time.month
            and date.day == t.date_time.day
            and date.hour == t.date_time.hour
            and date.minute == t.date_time.minute
            and date.second == t.date_time.second
        ):
            temp = t
            break
    if request.method == "POST":
        form = TemperatureForm(request.POST, instance=temp)
    else:
        form = TemperatureForm(instance=temp)
    return save_temp_form(
        request,
        form,
        record_id,
        "mypatients/observation_partials/partial_temp_update.html",
    )


def temp_delete(request, ward, record_id, temp_label):
    patient = ClinicalRecord.objects.get(pk=record_id)
    date = datetime.strptime(temp_label, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc
    )
    temps = Temperature.objects.filter(record=record_id)
    temp = Temperature.objects.first()
    for t in temps:
        if (
            date.year == t.date_time.year
            and date.month == t.date_time.month
            and date.day == t.date_time.day
            and date.hour == t.date_time.hour
            and date.minute == t.date_time.minute
            and date.second == t.date_time.second
        ):
            temp = t
            break
    data = dict()
    if request.method == "POST":
        temp.delete()
        data["form_is_valid"] = True
        temps = Temperature.objects.filter(record=record_id)
    else:
        context = {
            "record": patient,
            "temp": temp,
        }
        data["html_form"] = render_to_string(
            "mypatients/observation_partials/partial_temp_update.html",
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
        context = {
            "record": patient,
            "prescription": pr,
        }
        data["html_form"] = render_to_string(
            "mypatients/prescription_partials/partial_pr_delete.html",
            context,
            request=request,
        )
    return JsonResponse(data)
