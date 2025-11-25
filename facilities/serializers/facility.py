from rest_framework import serializers
from ..models import MedicalFacility

class MedicalFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFacility
        fields = ['id', 'code', 'name', 'facility_type', 'address', 'city', 'phone', 
                  'email', 'capacity', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_code(self, value):
        if ' ' in value:
            raise serializers.ValidationError('El código no debe contener espacios')
        return value