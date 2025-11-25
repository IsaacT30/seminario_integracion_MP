from django.contrib import admin
from medical_records.models import MedicalRecord, MedicalRecordDetail

class MedicalRecordDetailInline(admin.TabularInline):
    model = MedicalRecordDetail
    extra = 1
    readonly_fields = ('procedure_date',)

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('record_number', 'patient_name', 'patient_id_number', 'doctor', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient_name', 'patient_id_number', 'record_number', 'diagnosis')
    readonly_fields = ('record_number', 'total_cost', 'created_at', 'updated_at')
    inlines = [MedicalRecordDetailInline]

@admin.register(MedicalRecordDetail)
class MedicalRecordDetailAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'procedure', 'cost', 'procedure_date')
    list_filter = ('procedure_date',)
    search_fields = ('medical_record__patient_name', 'procedure__name')
