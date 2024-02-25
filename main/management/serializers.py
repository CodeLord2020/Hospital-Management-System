from rest_framework import serializers
from .models import MedicalHistory, Appointment, TestResult, Insurance
from humans.models import Patient

class MedicalHistoryListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='medical-history-details', lookup_field='pk')
    """
    Serializer for listing medical histories with limited information.
    """
    patient_id = serializers.SerializerMethodField()


    class Meta:
        model = MedicalHistory
        fields = ['patient_id', 'date_recorded', 'details']

    def get_patient_id(self, obj):
        return obj.patient.user.get_user_id()

class MedicalHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for detailed medical history information.
    """
    class Meta:
        model = MedicalHistory
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
    # patient_name = serializers.SerializerMethodField()
    # doctor_name = serializers.SerializerMethodField()

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
    
    # def create(self, validated_data):
    #     print("At least got here")
    #     get_patient_id = validated_data.get("patient")
    #     get_patient_id = get_patient_id.id
    #     print(f"patient_id: {get_patient_id}")
    #     appointment_date = validated_data.get('appointment_date')
    #     if get_patient_id:
    #         patient_instance = Patient.objects.get(id = get_patient_id)
    #         print(f"patient_username: {patient_instance}")
    #         if patient_instance:
    #             patient_instance.last_appointment = patient_instance.next_appointment
    #             patient_instance.next_appointment = appointment_date
    #             patient_instance.save()
    #     return super().create(validated_data)

class TestResultListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestResult
        fields = ['test_name', 'date_updated']

class TestResultListUpdateSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='testresult-detail', lookup_field='pk')
    class Meta:
        model = TestResult
        exclude = ('date_added', 'date_updated' )

class TestResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestResult
        fields = '__all__'




class InsuranceListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='insurance-detail', lookup_field='pk')
    class Meta:
        model = Insurance
        fields = ['id', 'patient', 'details'] 

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'