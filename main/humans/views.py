from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.renderers import JSONOpenAPIRenderer
# Create your views here.
from .models import Patient, Doctor
from .permissions import IsDoctorOrReadOnly, IsAMedicalStaff, IsADoctor, IsFinalAuthority
from .serializers import PatientSerializer,ListPatientSerializer, DoctorListSerializer, DoctorSerializer




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
    

from management.serializers import AppointmentListSerializer

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

