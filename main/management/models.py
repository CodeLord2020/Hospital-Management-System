from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from authentication.models import User
from authentication.emails import send_appointment_change_mail, send_appointment_mail

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

# @receiver(post_save, sender = Appointment)
# def send_appointment_mail_updates(sender, instance, **kwargs):
#     email = instance.patient.email
#     date = instance.appointment_date
#     doc = instance.doctor.get_full_name()

    # if kwargs.get('created'):
    #     send_appointment_mail(email, date, doc)
    #     print("Appointment mail sent")
    # elif kwargs.get('update_fields'):  # Check only if update_fields is not empty
    #     print("update_fields update mail sent")
    #     if "appointment_date" in kwargs['update_fields']:
    #         print("update_fields in kwargs update mail sent")
    #         send_appointment_change_mail(email, date, doc)
    #         print("Appointment update mail sent")
    # else:
    #     print("Pass update mail sent")
    # if kwargs.get('created'):
    #     send_appointment_mail(email, date, doc)
    #     print("Appointment mail sent")
    # # elif 'update_fields' in kwargs and kwargs['update_fields'] is not None and "appointment_date" in kwargs['update_fields']:
    # elif instance._state.adding or instance._state.db_record.appointment_date != instance.appointment_date:
    #     send_appointment_change_mail(email, date, doc)
    #     print("Appointment update mail sent")
    # else:
    #     pass
    

@receiver(pre_save, sender=Appointment)
def send_appointment_mail_updates(sender, instance, **kwargs):
    # Get the existing appointment instance from the database
    try:
        old_instance = Appointment.objects.get(pk=instance.pk)
    except Appointment.DoesNotExist:
        # If the instance is new and doesn't exist in the database yet, do nothing
        return

    email = instance.patient.email
    new_date = instance.appointment_date
    old_date = old_instance.appointment_date
    doc = instance.doctor.get_full_name()

    if instance.pk is None:
        # This is a new appointment
        send_appointment_mail(email, new_date, doc)
        print("Appointment mail sent")
    elif new_date != old_date:
        # The appointment_date field has been changed
        send_appointment_change_mail(email, new_date, doc)
        print("Appointment update mail sent")
    else:
        # No changes in the appointment_date field
        pass
    

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
    symtoms = models.TextField(null = True)
    diagnosis = models.TextField()
    medication_name = models.TextField()
    instructions = models.TextField(null = True)
    
    doctor = models.ForeignKey('humans.Doctor', on_delete=models.SET_NULL, null=True, related_name='medical_records')


    def __str__(self):
        return f"Medical history for {self.patient.user.get_full_name()} recorded on {self.date_recorded}"




class TestResult(models.Model):
    patient = models.ForeignKey('humans.Patient', on_delete=models.CASCADE, null = True)
    # medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    test_approved_by = models.CharField(max_length=100, null = True)
    tested_by = models.CharField(max_length=100, null = True)
    lab_name = models.CharField(max_length=100, null = True)

    result = models.TextField()
    
    date_added = models.DateTimeField(auto_now_add=True, null= True)
    date_updated = models.DateTimeField(auto_now=True, null= True)

    def __str__(self):
        return f"{self.test_name} test result for {self.patient.get_full_name()}"
