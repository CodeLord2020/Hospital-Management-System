from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status, generics

import logging
from .models import Appointment
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .paginator import appointmennt_paginator
from rest_framework.renderers import JSONOpenAPIRenderer
# Create your views here.
from .models import Patient, Doctor
from .permissions import IsDoctorOrReadOnly, IsAMedicalStaff, IsADoctor, IsFinalAuthority
from .serializers import PatientSerializer,ListPatientSerializer, DoctorListSerializer, DoctorSerializer, AppointmentCreateSerializer, AppointmentListSerializer, AppointmentSerializer




class PatientListView(ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = ListPatientSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]
    # renderer_classes = [JSONOpenAPIRenderer]

class CreatePatientView(CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]

class PatientDetailsView(RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsAMedicalStaff]

class UpdatePatientView(UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]

class DeletePatientView(DestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrReadOnly]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAMedicalStaff]
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer

class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsADoctor]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DoctorUpdateView(generics.UpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsADoctor]

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

class DoctorDeleteView(generics.DestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsFinalAuthority]

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)
    

class DoctorPatientsAPIView(generics.ListAPIView):
    serializer_class = PatientSerializer 

    def get_queryset(self):
        doctor_id = self.kwargs['pk']
        return Doctor.objects.get(pk=doctor_id).my_patients()

class DoctorAppointmentsAPIView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer 
    def get_queryset(self):
        doctor_id = self.kwargs['pk']
        return Doctor.objects.get(pk=doctor_id).my_appointments()



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
