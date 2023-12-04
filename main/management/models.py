from django.db import models

from authentication.models import User

# Create your models here.

class Appointment(models.Model):
    patient = models.ForeignKey('humans.Patient', related_name = 'patient_appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey('humans.Doctor', related_name= 'doctor_appointments', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['appointment_date']

    def __str__(self):
        return f"Appointment for {self.patient.user.get_full_name} with {self.doctor.user.get_full_name} on {self.appointment_date}"
    

class DoctorSpecialty(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Insurance(models.Model):
    
    patient = models.ForeignKey('humans.Patient', on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    coverage_details = models.TextField()

    def __str__(self):
        return f"Insurance for {self.patient.user.get_full_name()} with {self.provider_name}"


class MedicalFacility(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()

    def __str__(self):
        return self.name

class MedicalHistory(models.Model):
    patient = models.ForeignKey('humans.Patient', on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    prescription = models.TextField()
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='medical_records')

    def __str__(self):
        return f"Medical history for {self.patient.user.get_full_name()} recorded on {self.date_recorded}"


class Prescription(models.Model):
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField()

    def __str__(self):
        return f"Prescription for {self.medical_history.patient.user.get_full_name()} - {self.medication_name}"
    

class TestResult(models.Model):
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    result = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, null= True)
    date_updated = models.DateTimeField(auto_now=True, null= True)

    def __str__(self):
        return f"Test result for {self.medical_history.patient.user.get_full_name()} - {self.test_name}"
