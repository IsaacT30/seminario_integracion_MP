# medical_records/services/totals.py
from decimal import Decimal, ROUND_HALF_UP

def quantize(amount):
    return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def recompute_medical_record(record):
    """
    Recalcula el costo total de la historia clínica en base a los procedimientos realizados.
    """
    from medical_records.models import MedicalRecordDetail  # import local para evitar ciclos
    details = MedicalRecordDetail.objects.filter(medical_record=record)
    total = sum((Decimal(d.cost) for d in details), Decimal('0'))
    record.total_cost = quantize(total)
    record.save(update_fields=['total_cost'])
