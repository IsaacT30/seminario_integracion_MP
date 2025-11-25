from rest_framework import serializers
from medical_services.models import Specialty

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id","name","slug","description","created_at","updated_at")
        read_only_fields = ("id","created_at","updated_at")