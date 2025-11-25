from django.db import models

class MedicalFacility(models.Model):
    """Instalación o centro médico"""
    CLINIC = 'CLINIC'
    HOSPITAL = 'HOSPITAL'
    LABORATORY = 'LABORATORY'
    EMERGENCY = 'EMERGENCY'
    FACILITY_TYPE_CHOICES = [
        (CLINIC, 'Clínica'),
        (HOSPITAL, 'Hospital'),
        (LABORATORY, 'Laboratorio'),
        (EMERGENCY, 'Urgencias'),
    ]
    
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES, default=CLINIC)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    capacity = models.PositiveIntegerField(default=0, help_text="Capacidad de pacientes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Medical Facilities"
        
    def __str__(self):
        return f'{self.code} - {self.name}'
    