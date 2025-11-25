# medical_records/views/medical_record.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils.crypto import get_random_string

from medical_records.models import MedicalRecord
from medical_records.serializers.medical_record import MedicalRecordSerializer, MedicalRecordCreateSerializer
from medical_records.serializers.record_detail import MedicalRecordDetailSerializer
from medical_records.services.totals import recompute_medical_record

class IsDoctorOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.doctor_id == request.user.id

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('status','patient_id_number')
    search_fields = ('patient_name','patient_id_number','record_number','diagnosis')
    ordering_fields = ('created_at','patient_name')

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(doctor=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action in ('create','update','partial_update'):
            return MedicalRecordCreateSerializer
        return MedicalRecordSerializer

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

    @action(detail=True, methods=['post'])
    def add_procedure(self, request, pk=None):
        """Agrega un procedimiento a la historia clínica (solo si está en DRAFT o IN_PROGRESS)."""
        record = self.get_object()
        self.check_object_permissions(request, record)
        if record.status not in [MedicalRecord.DRAFT, MedicalRecord.IN_PROGRESS]:
            return Response({'detail':'Solo puedes agregar procedimientos en DRAFT o IN_PROGRESS'}, status=400)

        ser = MedicalRecordDetailSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(medical_record=record)
        recompute_medical_record(record)
        return Response(MedicalRecordSerializer(record).data)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def complete(self, request, pk=None):
        """Completa la historia clínica: asigna número de registro."""
        record = self.get_object()
        self.check_object_permissions(request, record)
        if record.status == MedicalRecord.COMPLETED:
            return Response({'detail':'La historia clínica ya está completada'}, status=400)

        # Asignar número de historia clínica
        if not record.record_number:
            record.record_number = f'HC-{get_random_string(8).upper()}'

        record.status = MedicalRecord.COMPLETED
        record.save(update_fields=['record_number','status'])
        recompute_medical_record(record)
        return Response(MedicalRecordSerializer(record).data, status=200)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def archive(self, request, pk=None):
        """Archiva la historia clínica."""
        record = self.get_object()
        self.check_object_permissions(request, record)
        if record.status == MedicalRecord.ARCHIVED:
            return Response({'detail':'La historia clínica ya está archivada'}, status=400)

        record.status = MedicalRecord.ARCHIVED
        record.save(update_fields=['status'])
        return Response(MedicalRecordSerializer(record).data, status=200)
