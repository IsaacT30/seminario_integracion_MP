# medical_records/views/medical_record.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils.crypto import get_random_string

from medical_records.models import MedicalRecord
from medical_records.serializers.medical_record import MedicalRecordSerializer, MedicalRecordCreateSerializer
from medical_records.serializers.record_detail import MedicalRecordDetailSerializer
from medical_records.services.totals import recompute_medical_record
from medical_records.permissions import CanManageMedicalRecords, IsOwnerOrDoctor, IsAdminOrDoctor

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    permission_classes = (permissions.IsAuthenticated, CanManageMedicalRecords)
    filterset_fields = ('status','patient_id_number')
    search_fields = ('patient_name','patient_id_number','record_number','diagnosis')
    ordering_fields = ('created_at','patient_name')

    def get_queryset(self):
        """
        Filtrar historias según el rol del usuario
        """
        qs = super().get_queryset()
        user = self.request.user
        
        # Si no tiene perfil, no ver nada
        if not hasattr(user, 'doctor_profile'):
            return qs.none()
        
        user_role = user.doctor_profile.role
        
        # Admin ve todas
        if user_role == 'ADMIN' or user.is_staff:
            return qs
        
        # Doctor solo ve las suyas
        if user_role == 'DOCTOR':
            return qs.filter(doctor=user)
        
        # Paciente solo ve las suyas (cuando se implemente patient_user)
        if user_role == 'PATIENT':
            # Por ahora retornar ninguna hasta que se agregue el campo patient_user
            return qs.none()
        
        # Otros roles no ven nada
        return qs.none()

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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdminOrDoctor])
    @transaction.atomic
    def complete(self, request, pk=None):
        """Completa la historia clínica: asigna número de registro."""
        record = self.get_object()
        
        # Verificar permisos adicionales
        if not request.user.is_staff and hasattr(request.user, 'doctor_profile'):
            if request.user.doctor_profile.role == 'DOCTOR' and record.doctor != request.user:
                return Response({'detail': 'No tienes permiso para completar esta historia clínica'}, status=403)
        
        if record.status == MedicalRecord.COMPLETED:
            return Response({'detail':'La historia clínica ya está completada'}, status=400)

        # Asignar número de historia clínica
        if not record.record_number:
            record.record_number = f'HC-{get_random_string(8).upper()}'

        record.status = MedicalRecord.COMPLETED
        record.save(update_fields=['record_number','status'])
        recompute_medical_record(record)
        return Response(MedicalRecordSerializer(record).data, status=200)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdminOrDoctor])
    @transaction.atomic
    def archive(self, request, pk=None):
        """Archiva la historia clínica."""
        record = self.get_object()
        
        # Verificar permisos adicionales
        if not request.user.is_staff and hasattr(request.user, 'doctor_profile'):
            if request.user.doctor_profile.role == 'DOCTOR' and record.doctor != request.user:
                return Response({'detail': 'No tienes permiso para archivar esta historia clínica'}, status=403)
        
        if record.status == MedicalRecord.ARCHIVED:
            return Response({'detail':'La historia clínica ya está archivada'}, status=400)

        record.status = MedicalRecord.ARCHIVED
        record.save(update_fields=['status'])
        return Response(MedicalRecordSerializer(record).data, status=200)
