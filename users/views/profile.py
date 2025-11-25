# users/views/profile.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import DoctorProfile
from users.serializers.profile import DoctorProfileSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.select_related('user').all()
    serializer_class = DoctorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            # Los usuarios no staff solo pueden ver su propio perfil
            qs = qs.filter(user=self.request.user)
        return qs
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener el perfil del usuario actual"""
        try:
            profile = DoctorProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except DoctorProfile.DoesNotExist:
            return Response({'detail': 'Perfil no encontrado'}, status=404)
