from rest_framework import serializers
from django.utils.text import slugify
from medical_services.models import Specialty

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id","name","slug","description","created_at","updated_at")
        read_only_fields = ("id","slug","created_at","updated_at")
    
    def create(self, validated_data):
        # Auto-generar slug desde el nombre si no se proporciona
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Auto-generar slug si el nombre cambia
        if 'name' in validated_data and validated_data['name'] != instance.name:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)