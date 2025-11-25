from rest_framework import viewsets, filters
from medical_services.models import MedicalProcedure
from medical_services.serializers import MedicalProcedureSerializer
from medical_services.permissions import IsAdminOrReadOnly
from medical_services.pagination import StandardResultsSetPagination

class MedicalProcedureViewSet(viewsets.ModelViewSet):
    queryset = MedicalProcedure.objects.select_related("specialty").all()
    serializer_class = MedicalProcedureSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name","slug","code","specialty__name")
    ordering_fields = ("cost","created_at","name")

    def get_queryset(self):
        qs = super().get_queryset()
        specialty = self.request.query_params.get("specialty")
        is_active = self.request.query_params.get("is_active")
        if specialty:
            qs = qs.filter(specialty__id=specialty)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() in ("1","true","t","yes"))
        return qs