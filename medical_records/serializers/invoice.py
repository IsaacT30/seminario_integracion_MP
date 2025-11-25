# medical_records/serializers/invoice.py
from rest_framework import serializers
from medical_records.models import MedicalRecord, MedicalRecordDetail

class MedicalRecordSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ('id','record_number','patient_name','patient_id_number','patient_birth_date',
                  'patient_phone','patient_email','patient_address','diagnosis','symptoms',
                  'observations','status','total_cost','created_at','updated_at','details')
        read_only_fields = ('id','record_number','total_cost','created_at','updated_at','details')

    def get_details(self, obj):
        qs = MedicalRecordDetail.objects.filter(medical_record=obj).select_related('procedure')
        from medical_records.serializers.detail import MedicalRecordDetailSerializer
        return MedicalRecordDetailSerializer(qs, many=True).data

class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ('patient_name','patient_id_number','patient_birth_date','patient_phone',
                  'patient_email','patient_address','diagnosis','symptoms','observations')
