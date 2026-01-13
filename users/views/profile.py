# users/views/profile.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import DoctorProfile
from users.serializers.profile import DoctorProfileSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar perfiles de usuario.
    - Usuarios normales: Solo pueden ver/editar su propio perfil
    - ADMIN: Pueden ver y editar todos los perfiles
    """
    queryset = DoctorProfile.objects.select_related('user').all()
    serializer_class = DoctorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        """
        Filtrar perfiles según el rol del usuario
        """
        qs = super().get_queryset()
        user = self.request.user
        
        # Admin puede ver todos los perfiles
        if user.is_staff:
            return qs
        
        # Verificar si tiene perfil y es ADMIN
        if hasattr(user, 'doctor_profile') and user.doctor_profile.role == 'ADMIN':
            return qs
        
        # Otros usuarios solo ven su propio perfil
        return qs.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener el perfil del usuario actual"""
        try:
            profile = DoctorProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except DoctorProfile.DoesNotExist:
            return Response({'detail': 'Perfil no encontrado'}, status=404)
