from .models import Patient, Doctor
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