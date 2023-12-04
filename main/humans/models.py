from django.db import models
from authentication.models import User
from management.models import MedicalFacility, DoctorSpecialty
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

    

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_facility = models.ForeignKey(MedicalFacility, on_delete=models.CASCADE)
    specialties = models.ManyToManyField(DoctorSpecialty, related_name= 'doctor_specialties')
    bio = models.TextField(blank=True, null=True)
    
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    date_added = models.DateTimeField(auto_now_add=True, null= True)
    date_updated = models.DateTimeField(auto_now=True, null= True)

    def my_patients(self):
        return self.patients_attending.all()
    
    def my_appointments(self):
        return self.doctor_appointments.all()
    
    def get_full_name(self):
        return self.user.get_full_name

    
    def __str__(self):
        # return f"Doctor {self.id}"
        if self.user:
            return self.user.get_full_name
        else:
            return f"Doctor {self.id}"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0, 'Age must be greater than or equal to zero'),
            MaxValueValidator(150, 'Age is unrealistic')
        ],
        blank=False,
        null=False
    )
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],)
    address = models.TextField()
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    doctors = models.ManyToManyField(Doctor, related_name='patients_attending', blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    pre_existing_conditions = models.TextField(blank=True, null=True)
    
    last_appointment = models.DateTimeField(null= True, blank= True)
    next_appointment = models.DateTimeField(null= True, blank= True)

    date_added = models.DateTimeField(auto_now_add=True, null= True)
    date_updated = models.DateTimeField(auto_now=True, null= True)

    def my_appointments(self):
        return self.patient_appointments.all()
    

    def get_full_name(self):
        return self.user.get_full_name

    def __str__(self):
        return self.user.get_full_name