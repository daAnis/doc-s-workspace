from django import forms

from .models import Examination, Prescription, Pressure, Temperature, ClinicalRecord

DATE_INPUT_FORMATS = [
    "%Y-%m-%d",
]


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
        )
