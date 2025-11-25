# users/serializers/profile.py
from rest_framework import serializers
from users.models import DoctorProfile
from django.contrib.auth.models import User

class DoctorProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DoctorProfile
        fields = ('id', 'user', 'username', 'email', 'full_name', 'role', 
                  'license_number', 'specialization', 'phone', 'bio', 
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
