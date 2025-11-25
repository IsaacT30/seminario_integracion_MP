# billing_api/urls.py
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Sistema de Historias Clínicas"
admin.site.site_title = "Admin Historias Clínicas"
admin.site.index_title = "Administración del Sistema Médico"

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', include('users.urls')),     
  path('api/', include('medical_services.urls')),    
  path('api/', include('medical_records.urls')),
  path('api/', include('facilities.urls')),
]
