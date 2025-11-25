# medical_records/signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from medical_records.models import MedicalRecordDetail
from medical_records.services.totals import recompute_medical_record

@receiver(pre_save, sender=MedicalRecordDetail)
def set_detail_cost(sender, instance: MedicalRecordDetail, **kwargs):
    """Establece el costo del procedimiento si no se ha proporcionado"""
    if not instance.cost:
        instance.cost = instance.procedure.cost

@receiver(post_save, sender=MedicalRecordDetail)
def recompute_after_detail_save(sender, instance: MedicalRecordDetail, created, **kwargs):
    recompute_medical_record(instance.medical_record)

@receiver(post_delete, sender=MedicalRecordDetail)
def recompute_after_detail_delete(sender, instance: MedicalRecordDetail, **kwargs):
    recompute_medical_record(instance.medical_record)
