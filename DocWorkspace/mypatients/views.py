from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, FileResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from docx import Document
from htmldocx import HtmlToDocx
from io import BytesIO

from datetime import date, datetime, timezone

from .models import (
    ClinicalRecord,
    Examination,
    Temperature,
    Pressure,
    Prescription,
    Patient,
    Diary,
    Notification,
)
from .forms import (
    ExaminationForm,
    PrescriptionForm,
    PressureForm,
    TemperatureForm,
    RecordForm,
    DiariesFormSet,
    PatientForm,
)

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(doctor=request.user).order_by('-date_time')
    data = dict()
    data["html_notifications"] = render_to_string(
                "mypatients/shared_partials/partial_notifications_list.html",
                {
                    "notifications": notifications
                },
            )
    return JsonResponse(data)


@login_required
def wards(request):
    records = ClinicalRecord.objects.filter(doctor=request.user)
    wards = set()
    for r in records:
        wards.add(r.ward)
    s_wards = sorted(wards)
    return render(request, "mypatients/wards.html", {"wards": s_wards})


@login_required
def records_in_ward(request, ward):
    records = ClinicalRecord.objects.filter(ward=ward)
    return render(
        request, "mypatients/patients.html", {"records": records, "ward": ward}
    )


@login_required
def record(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    human = Patient.objects.get(pk=patient.patient.pk)
    form = RecordForm(instance=patient)
    human_form = PatientForm(instance=human)
    diaries = DiariesFormSet(instance=patient)
    context = {
        "record": patient,
        "form": form,
        "human_form": human_form,
        "diaries": diaries,
    }
    return render(request, "mypatients/patient.html", context)


@login_required
def patient_update(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    human = Patient.objects.get(pk=patient.patient.pk)
    recived_human_form = PatientForm(request.POST, instance=human)
    if recived_human_form.is_valid():
        if recived_human_form.has_changed():
            recived_human_form.save()
    context = {"ward": ward, "record_id": record_id}
    redirect_url = reverse("record", kwargs=context)
    return HttpResponseRedirect(redirect_url)


@login_required
def record_update(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    recived_form = RecordForm(request.POST, instance=patient)
    print(recived_form)
    if recived_form.is_valid():
        if recived_form.has_changed():
            form = recived_form.save(commit=False)
            if not form.primary_diagnosis:
                form.primary_diagnosis = form.preliminary_diagnosis
            form.save()
    context = {"ward": ward, "record_id": record_id}
    redirect_url = reverse("record", kwargs=context)
    return HttpResponseRedirect(redirect_url)


@login_required
def diaries_update(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    formset = DiariesFormSet(request.POST, instance=patient)
    if formset.is_valid():
        formset.save()
    else:
        print(formset.errors)
    context = {"ward": ward, "record_id": record_id}
    redirect_url = reverse("record", kwargs=context)
    return HttpResponseRedirect(redirect_url)


@login_required
def get_discharge(request, ward, record_id):
    record = ClinicalRecord.objects.get(pk=record_id)
    examination_list = Examination.objects.filter(record=record_id)
    prescription_list = Prescription.objects.filter(record=record_id)
    context = {
        "record": record,
        "examination_list": examination_list,
        "prescription_list": prescription_list,
    }
    template = render_to_string("mypatients/document_templates/discharge.html", context)
    document = Document()
    new_parser = HtmlToDocx()
    byte_io = BytesIO()
    new_parser.add_html_to_document(template, document)
    document.save(byte_io)
    record.discharge.delete()
    byte_io.seek(0)
    record.discharge.save("Выписка.docx", ContentFile(byte_io.read()))
    data = dict()
    data["html_template"] = template
    return JsonResponse(data)


@login_required
def examination(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    exam_list = Examination.objects.filter(record=record_id)
    return render(
        request,
        "mypatients/examination.html",
        {"record": patient, "examinations": exam_list},
    )


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def observation(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    temps = Temperature.objects.filter(record=record_id)
    bpps = Pressure.objects.filter(record=record_id)
    return render(
        request,
        "mypatients/observation.html",
        {"record": patient, "temps": temps, "bpps": bpps},
    )


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def temp_update_get(request, ward, record_id, temp_label):
    date = datetime.strptime(temp_label, "%Y-%m-%dT%H:%M:%S.%fZ")
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
    form = TemperatureForm(instance=temp)
    patient = ClinicalRecord.objects.get(pk=record_id)
    data = dict()
    context = {"form": form, "record": patient, "temp": temp}
    data["html_form"] = render_to_string(
        "mypatients/observation_partials/partial_temp_update.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
def temp_update_post(request, ward, record_id, temp_id):
    temp = Temperature.objects.get(pk=temp_id)
    form = TemperatureForm(request.POST, instance=temp)
    patient = ClinicalRecord.objects.get(pk=record_id)
    data = dict()
    if form.is_valid():
        recived_form = form.save(commit=False)
        recived_form.record = patient
        recived_form.save()
        data["form_is_valid"] = True
        temps = Temperature.objects.filter(record=record_id)
    else:
        data["form_is_valid"] = False
    context = {"form": form, "record": patient, "temp": temp}
    data["html_form"] = render_to_string(
        "mypatients/observation_partials/partial_temp_update.html",
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
def temp_delete(request, ward, record_id, temp_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    temp = Temperature.objects.get(pk=temp_id)
    data = dict()
    if request.method == "POST":
        temp.delete()
        data["form_is_valid"] = True
    else:
        context = {
            "record": patient,
            "temp": temp,
        }
        data["html_form"] = render_to_string(
            "mypatients/observation_partials/partial_temp_delete.html",
            context,
            request=request,
        )
    return JsonResponse(data)


@login_required
def prescription(request, ward, record_id):
    patient = ClinicalRecord.objects.get(pk=record_id)
    presc_list = Prescription.objects.filter(record=record_id)
    return render(
        request,
        "mypatients/prescription.html",
        {"record": patient, "prescriptions": presc_list},
    )


@login_required
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


@login_required
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


@login_required
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


@login_required
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
