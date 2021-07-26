from django import forms
from django.db.models import fields
from django.forms import inlineformset_factory

from .models import (
    Examination,
    Prescription,
    Pressure,
    Temperature,
    ClinicalRecord,
    Diary,
    Patient,
)

DATE_INPUT_FORMATS = [
    "%Y-%m-%d",
]


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ("date_time", "complaint", "status_p_c", "status_localis")


DiariesFormSet = inlineformset_factory(
    ClinicalRecord,
    Diary,
    form=DiaryForm,
    extra=1,
    can_order=True,
)


class ExaminationForm(forms.ModelForm):
    class Meta:
        model = Examination
        fields = ("name",)


class PrescriptionForm(forms.ModelForm):
    date_1 = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    date_2 = forms.DateField(input_formats=DATE_INPUT_FORMATS)

    class Meta:
        model = Prescription
        fields = (
            "name",
            "date_1",
            "date_2",
        )


class PressureForm(forms.ModelForm):
    class Meta:
        model = Pressure
        fields = (
            "diastole",
            "systole",
            "puls",
        )


class TemperatureForm(forms.ModelForm):
    class Meta:
        model = Temperature
        fields = ("value",)


class RecordForm(forms.ModelForm):
    class Meta:
        model = ClinicalRecord
        fields = (
            "complaint",
            "anamnesis",
            "habitual_intoxication",
            "occupational_hazards",
            "epidanamnesis",
            "allergic_history",
            "blood_transfusion",
            "expert_history",
            "past_illnesses",
            "status_p_c",
            "respiratory_system",
            "circulatory_organs",
            "digestive_organs",
            "urinary_organs",
            "status_localis",
            "preliminary_diagnosis",
            "primary_diagnosis",
            "data_from_additional_research_methods",
            "recommendation",
        )


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ("name", "birth_date", "phone_number", "address", "height", "weight",)


class PatientSearchForm(forms.ModelForm):
    CHOICES = [
        ('mine', 'Мои пациенты'),
        ('all', 'Все пациенты')
    ]

    whose_patients = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    archive = forms.BooleanField()

    class Meta:
        model = Patient
        fields = ("name", "whose_patients", "archive")

    def __init__(self, *args, **kwargs):
        self.fields['whose_patients'].initial = self.CHOICES[0]
        super(PatientSearchForm, self).__init__(*args, **kwargs)