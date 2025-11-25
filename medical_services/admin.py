from django.contrib import admin
from medical_services.models import Specialty, MedicalProcedure

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(MedicalProcedure)
class MedicalProcedureAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'specialty', 'cost', 'duration_minutes', 'is_active')
    list_filter = ('specialty', 'is_active')
    search_fields = ('name', 'code', 'specialty__name')
    prepopulated_fields = {'slug': ('name',)}
