# medical_records/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permiso: Solo administradores
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and hasattr(request.user, 'doctor_profile')
            and request.user.doctor_profile.role == 'ADMIN'
        )


class IsAdminOrDoctor(permissions.BasePermission):
    """
    Permiso: Administradores y Doctores
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not hasattr(request.user, 'doctor_profile'):
            return False
        
        return request.user.doctor_profile.role in ['ADMIN', 'DOCTOR']


class IsOwnerOrDoctor(permissions.BasePermission):
    """
    Permiso: El dueño del recurso, el doctor asignado, o un admin
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not hasattr(request.user, 'doctor_profile'):
            return False
        
        user_role = request.user.doctor_profile.role
        
        # Admins pueden ver todo
        if user_role == 'ADMIN':
            return True
        
        # Doctores solo ven sus propias historias
        if user_role == 'DOCTOR':
            return obj.doctor == request.user
        
        # Pacientes solo ven sus propias historias
        # (Requiere agregar campo patient_user al modelo en el futuro)
        if user_role == 'PATIENT':
            return hasattr(obj, 'patient_user') and obj.patient_user == request.user
        
        return False


class CanManageMedicalRecords(permissions.BasePermission):
    """
    Permiso: Crear/editar historias clínicas (Admin y Doctor)
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not hasattr(request.user, 'doctor_profile'):
            return False
        
        # Solo lectura para todos autenticados
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Crear/Editar solo Admin y Doctor
        return request.user.doctor_profile.role in ['ADMIN', 'DOCTOR']


class CanManageCatalogs(permissions.BasePermission):
    """
    Permiso: Gestionar catálogos (Especialidades, Procedimientos, etc)
    Solo Admins
    """
    def has_permission(self, request, view):
        # Lectura para todos autenticados
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Escritura solo para Admins
        return (
            request.user 
            and request.user.is_authenticated 
            and hasattr(request.user, 'doctor_profile')
            and request.user.doctor_profile.role == 'ADMIN'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso: Admins pueden modificar, otros solo pueden leer
    """
    def has_permission(self, request, view):
        # Lectura permitida para todos los autenticados
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Escritura solo para Admins
        return (
            request.user 
            and request.user.is_authenticated 
            and hasattr(request.user, 'doctor_profile')
            and request.user.doctor_profile.role == 'ADMIN'
        )
