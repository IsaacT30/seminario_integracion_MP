from rest_framework.routers import DefaultRouter
from medical_services.views.specialty import SpecialtyViewSet
from medical_services.views.procedure import MedicalProcedureViewSet

router = DefaultRouter()
router.register(r'specialties', SpecialtyViewSet, basename='specialty')
router.register(r'procedures', MedicalProcedureViewSet, basename='procedure')

urlpatterns = router.urls