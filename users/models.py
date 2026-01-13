from django.db import models
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    """Perfil extendido para usuarios del sistema"""
    DOCTOR = 'DOCTOR'
    NURSE = 'NURSE'
    ADMIN = 'ADMIN'
    RECEPTIONIST = 'RECEPTIONIST'
    PATIENT = 'PATIENT'
    ROLE_CHOICES = [
        (DOCTOR, 'Médico'),
        (NURSE, 'Enfermero/a'),
        (ADMIN, 'Administrativo'),
        (RECEPTIONIST, 'Recepcionista'),
        (PATIENT, 'Paciente'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=DOCTOR)
    license_number = models.CharField(max_length=50, blank=True, help_text="Número de licencia médica")
    specialization = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True, help_text="Biografía profesional")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"
