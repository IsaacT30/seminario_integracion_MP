from django.contrib import admin
from users.models import DoctorProfile

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'license_number', 'specialization', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'license_number', 'specialization')
    raw_id_fields = ('user',)