from django.shortcuts import render
from datetime import timezone
from humans.models import Patient
import logging
from .models import MedicalHistory, Appointment, TestResult, Insurance
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .paginator import appointmennt_paginator
from .permissions import IsADoctor, IsAMedicalStaff, IsDoctorOrReadOnly
from .serializers import (MedicalHistoryListSerializer, MedicalHistorySerializer,
                           AppointmentListSerializer, AppointmentSerializer, AppointmentCreateSerializer,
                             TestResultSerializer, TestResultListSerializer, TestResultListUpdateSerializer,
                              InsuranceListSerializer, InsuranceSerializer )
# Create your views here.






class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]
    
    
    def perform_create(self, serializer):
        print("At least got here")
        get_patient_id = self.request.data.get("patient", None)
        print(f"patient_id: {get_patient_id}")
        appointment_date = self.request.data.get('appointment_date')
        if get_patient_id:
            try:
                patient_instance = Patient.objects.get(id = get_patient_id)
                print(f"patient_username: {patient_instance}")
                if patient_instance:
                    patient_instance.last_appointment = patient_instance.next_appointment
                    print (f'patient {patient_instance.last_appointment}')
                    patient_instance.next_appointment = appointment_date
                    print (f'patient {patient_instance.next_appointment}')
                    patient_instance.save()
            except ObjectDoesNotExist:
                logging.error("Patients model instance not found")

        serializer.save()


    # def post(self, request, *args, **kwargs):
    #     print("At least got here (views)")
    #     get_patient_id = self.request.data.get("patient", None)
    #     print(f"(views)patient_id: {get_patient_id}")
    #     appointment_date = self.request.data.get('appointment_date')
    #     if get_patient_id:
    #         patient_instance = Patient.objects.get(id = get_patient_id)
    #         print(f"patient_username(views): {patient_instance}")
    #         if patient_instance:
    #             patient_instance.last_appointment = patient_instance.next_appointment
    #             patient_instance.next_appointment = appointment_date
    #     return super().post(request, *args, **kwargs)
    


class AppointmentListView(generics.ListAPIView):
    """
    List all appointments for a patient or doctor.
    Accessible to all medical staff.
    """
    serializer_class = AppointmentListSerializer
    permission_classes = [permissions.IsAuthenticated,IsADoctor]  
    pagination_class = appointmennt_paginator

    def get_queryset(self):
        return Appointment.objects.all()

class AppointmentRetrieveView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific appointment.
    Accessible to all medical staff.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAMedicalStaff]

class AppointmentScheduleView(generics.CreateAPIView):
    """
    Schedule a new appointment.
    Accessible to all medical staff.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAMedicalStaff]

class AppointmentUpdateView(generics.UpdateAPIView):
    """
    Update an existing appointment.
    Accessible to all medical staff.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAMedicalStaff]







class InsuranceList(generics.ListAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceListSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]


class InsuranceDetail(generics.RetrieveAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]
    

class InsuranceCreate(generics.CreateAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]


class InsuranceUpdate(generics.UpdateAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]


class InsuranceDelete(generics.DestroyAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]







class MedicalHistoryListView(generics.ListCreateAPIView):
    """
    List all medical histories for a patient or create a new medical history entry.
    """
    serializer_class = MedicalHistoryListSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]

class MedicalHistoryDetailsView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific medical history entry.
    Only accessible to medical staff.
    """
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAMedicalStaff]

class MedicalHistoryCreateView(generics.CreateAPIView):
    """
    Create a new medical history entry.
    Only accessible to medical staff.
    """
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAMedicalStaff]

    def perform_create(self, serializer):
        # Automatically set the doctor field to the current user (assuming doctors are users)
        serializer.save(doctor=self.request.user)

class MedicalHistoryUpdateView(generics.UpdateAPIView):
    """
    Update a specific medical history entry.
    Only accessible to medical staff.
    """
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAMedicalStaff]

class MedicalHistoryDeleteView(generics.DestroyAPIView):
    """
    Delete a specific medical history entry.
    Only accessible to medical staff.
    """
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsADoctor]







class TestResultListAPIView(generics.ListAPIView):

    serializer_class = TestResultListSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]
    queryset = TestResult.objects.all

    def get_queryset(self):

         # Assuming the patient ID is passed as a query parameter
        patient_id = self.request.query_params.get('patient_id', None)

        if patient_id:
            return TestResult.objects.filter(medical_history__patient__id=patient_id)
        else:
            return TestResult.objects.all()


class TestResultDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific test result.
    """
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]

class TestResultCreateAPIView(generics.CreateAPIView):
    """
    API view to upload a new test result.
    """
    serializer_class = TestResultListUpdateSerializer
    permission_classes = [IsAuthenticated,IsAMedicalStaff]

    def perform_create(self, serializer):
        # Assuming the patient ID is passed as a query parameter
        patient_id = self.request.data.get('patient_id', None)
        serializer.save(medical_history__patient_id=patient_id, date_added=timezone.now())

class TestResultUpdateAPIView(generics.UpdateAPIView):
    """
    API view to update a test result.
    """
    queryset = TestResult.objects.all()
    serializer_class = TestResultListUpdateSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]
    
    def perform_update(self, serializer):
        serializer.save(date_updated=timezone.now())

class TestResultDeleteAPIView(generics.DestroyAPIView):
    """
    API view to delete a test result.
    """
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated, IsADoctor]

    



