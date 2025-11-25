# medical_records/models/record_detail.py
from django.db import models
from medical_services.models import MedicalProcedure
from .medical_record import MedicalRecord

class MedicalRecordDetail(models.Model):
    """Detalle de procedimientos realizados en una historia clínica"""
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='details')
    procedure = models.ForeignKey(MedicalProcedure, on_delete=models.PROTECT)
    notes = models.TextField(blank=True, help_text="Notas específicas sobre el procedimiento realizado")
    procedure_date = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # costo copiado al momento

    def __str__(self):
        return f'{self.procedure} - {self.medical_record.patient_name}'
