from django.contrib import admin

from .models import Doctor, Notification, Patient, ClinicalRecord, Temperature, Pressure, Examination, Prescription

admin.site.register(Doctor)
admin.site.register(Notification)
admin.site.register(Patient)
admin.site.register(ClinicalRecord)
admin.site.register(Temperature)
admin.site.register(Pressure)
admin.site.register(Examination)
admin.site.register(Prescription)