from django.contrib import admin

from .models import Notification, Patient, ClinicalRecord, Temperature, Pressure, Examination, Prescription, Diary

admin.site.register(Notification)
admin.site.register(Patient)
admin.site.register(ClinicalRecord)
admin.site.register(Temperature)
admin.site.register(Pressure)
admin.site.register(Examination)
admin.site.register(Prescription)
admin.site.register(Diary)