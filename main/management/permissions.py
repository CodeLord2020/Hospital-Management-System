# permissions.py

from rest_framework import permissions

class IsDoctorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only doctors to perform certain actions on patients.
    """

    def has_permission(self, request, view):
        # Allow any GET request (list view)
        if request.method == 'GET':
            return True

        # Check if the user is a doctor
        return request.user.is_authenticated and request.user.is_doctor

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any user (GET, HEAD, OPTIONS requests)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is a doctor attending to the patient
        return request.user.is_authenticated and request.user.is_doctor and request.user in obj.doctors.all()

class IsADoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and  request.user.is_medical_staff and request.user.is_doctor 
    

class IsAMedicalStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_medical_staff 