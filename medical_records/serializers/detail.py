# medical_records/serializers/detail.py
from rest_framework import serializers
from medical_records.models import MedicalRecordDetail
from medical_services.models import MedicalProcedure

class MedicalRecordDetailSerializer(serializers.ModelSerializer):
    procedure_id = serializers.PrimaryKeyRelatedField(
        source='procedure', queryset=MedicalProcedure.objects.all(), write_only=True
    )
    procedure_name = serializers.ReadOnlyField(source='procedure.name')
    procedure_code = serializers.ReadOnlyField(source='procedure.code')

    class Meta:
        model = MedicalRecordDetail
        fields = ('id','medical_record','procedure_id','procedure_name','procedure_code',
                  'notes','procedure_date','cost')
        read_only_fields = ('id','procedure_name','procedure_code','procedure_date')
