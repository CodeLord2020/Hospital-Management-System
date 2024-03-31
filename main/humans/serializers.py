from .models import Patient, Doctor, Appointment
from rest_framework import serializers



class ListPatientSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='patient-detail', lookup_field='pk')

    class Meta:
        model = Patient
        fields = ['user', 'age', 'gender', 'details']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


# from management.serializers import DoctorSpecialtySerializer()
class DoctorListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='doctor-detail', lookup_field='pk')
    # specialties = DoctorSpecialtySerializer(many = True)
    class Meta:
        model = Doctor
        fields = ['id', 'medical_facility', 'details']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class AppointmentListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='appointment-detail', lookup_field='pk')
    # patient_name = serializers.SerializerMethodField()
    # doctor_name = serializers.SerializerMethodField()
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    class Meta:
        model = Appointment
        fields = ['id', 'patient_name', 'doctor_name', 'appointment_date', 'details']

    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name

    def get_doctor_name(self, obj):
        return obj.doctor.get_full_name
    

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'appointment_date', 'reason', 'is_confirmed', 'notes', 'patient_name', 'doctor_name']

    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name

    def get_doctor_name(self, obj):
        return obj.doctor.get_full_name
    
    
class AppointmentCreateSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    patient = serializers.IntegerField

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointment_date', 'reason', 'is_confirmed', 'notes', 'patient_name', 'doctor_name']

    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name

    def get_doctor_name(self, obj):
        return obj.doctor.get_full_name

