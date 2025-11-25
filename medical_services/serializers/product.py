from rest_framework import serializers
from medical_services.models import MedicalProcedure, Specialty

class MedicalProcedureSerializer(serializers.ModelSerializer):
    specialty_name = serializers.ReadOnlyField(source="specialty.name")
    specialty_id = serializers.PrimaryKeyRelatedField(
        source="specialty", queryset=Specialty.objects.all(), write_only=True
    )

    class Meta:
        model = MedicalProcedure
        fields = ("id","name","slug","code","description","cost","duration_minutes","is_active",
                  "specialty_id","specialty_name","created_at","updated_at")
        read_only_fields = ("id","created_at","updated_at","specialty_name")