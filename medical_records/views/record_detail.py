# medical_records/views/record_detail.py
from rest_framework import viewsets, permissions
from medical_records.models import MedicalRecordDetail
from medical_records.serializers.record_detail import MedicalRecordDetailSerializer

class MedicalRecordDetailViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecordDetail.objects.select_related('medical_record','procedure').all()
    serializer_class = MedicalRecordDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        return qs.filter(medical_record__doctor=user)

    def perform_create(self, serializer):
        record = serializer.validated_data.get('medical_record')
        if (not self.request.user.is_staff) and record.doctor != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('No puedes modificar historias clínicas de otros médicos')
        if record.status not in [record.DRAFT, record.IN_PROGRESS]:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Solo puedes agregar procedimientos cuando la historia está en DRAFT o IN_PROGRESS')
        serializer.save()
