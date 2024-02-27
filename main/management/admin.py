from django.contrib import admin

# Register your models here.

from .models import Appointment, DoctorSpecialty, Insurance, MedicalFacility, MedicalHistory, TestResult

admin.site.register(Appointment)
admin.site.register(DoctorSpecialty)
admin.site.register(Insurance)
admin.site.register(MedicalFacility)
admin.site.register(MedicalHistory)
# admin.site.register(Prescription)
admin.site.register(TestResult)
