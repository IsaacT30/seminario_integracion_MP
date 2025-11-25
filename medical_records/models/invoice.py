# medical_records/models/invoice.py
from django.db import models
from django.contrib.auth.models import User

class MedicalRecord(models.Model):
    """Historia clínica de un paciente"""
    DRAFT = 'DRAFT'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    ARCHIVED = 'ARCHIVED'
    STATUS_CHOICES = [
        (DRAFT, 'Borrador'),
        (IN_PROGRESS, 'En Progreso'),
        (COMPLETED, 'Completada'),
        (ARCHIVED, 'Archivada'),
    ]

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    record_number = models.CharField(max_length=32, unique=True, blank=True)  # asignado al completar
    patient_name = models.CharField(max_length=160)
    patient_id_number = models.CharField(max_length=50, help_text="Número de identificación del paciente")
    patient_birth_date = models.DateField()
    patient_phone = models.CharField(max_length=20, blank=True)
    patient_email = models.EmailField(blank=True)
    patient_address = models.TextField(blank=True)
    
    diagnosis = models.TextField(blank=True, help_text="Diagnóstico principal")
    symptoms = models.TextField(blank=True, help_text="Síntomas reportados")
    observations = models.TextField(blank=True, help_text="Observaciones del médico")
    
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=DRAFT)

    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Historia Clínica #{self.id} - {self.patient_name}'
