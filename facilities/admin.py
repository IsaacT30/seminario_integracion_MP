from django.contrib import admin
from facilities.models import MedicalFacility

@admin.register(MedicalFacility)
class MedicalFacilityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'facility_type', 'city', 'capacity', 'is_active', 'created_at')
    list_filter = ('facility_type', 'is_active', 'city')
    search_fields = ('code', 'name', 'city', 'address')
    list_editable = ('is_active',)
