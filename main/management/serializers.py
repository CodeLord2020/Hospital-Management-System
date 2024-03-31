from rest_framework import serializers
from .models import MedicalHistory, TestResult, Insurance





class InsuranceListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='insurance-detail', lookup_field='pk')
    class Meta:
        model = Insurance
        fields = ['id', 'patient', 'details'] 

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'







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







class TestResultListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestResult
        fields = ['test_name',  'test_approved_by', 'date_updated']


class TestResultListUpdateSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='testresult-detail', lookup_field='pk')
    class Meta:
        model = TestResult
        exclude = ('date_added', 'date_updated' )


class TestResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestResult
        fields = '__all__'



