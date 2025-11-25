from rest_framework import viewsets, filters
from medical_services.models import Specialty
from medical_services.serializers import SpecialtySerializer
from medical_services.permissions import IsAdminOrReadOnly

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name","slug","description")
    ordering_fields = ("name","created_at")