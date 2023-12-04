from django.urls import path
from .views import PatientListView, DeletePatientView, UpdatePatientView, CreatePatientView, PatientDetailsView
from .views import (
    DoctorListView,
    DoctorDetailView,
    DoctorCreateView,
    DoctorUpdateView,
    DoctorDeleteView,
)

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', PatientDetailsView.as_view(), name='patient-detail'),
    path('patients/create/', CreatePatientView.as_view(), name='create-patient'),
    path('patients/update/<int:pk>/', UpdatePatientView.as_view(), name='update-patient'),
    path('patients/delete/<int:pk>/', DeletePatientView.as_view(), name='delete-patient'),

    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('doctors/update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('doctors/delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor-delete'),


]