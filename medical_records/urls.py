# medical_records/urls.py
from rest_framework.routers import DefaultRouter
from medical_records.views.medical_record import MedicalRecordViewSet
from medical_records.views.record_detail import MedicalRecordDetailViewSet

router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet, basename='medical-record')
router.register(r'medical-record-details', MedicalRecordDetailViewSet, basename='medical-record-detail')

urlpatterns = router.urls
