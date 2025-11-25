from django.urls import path
from . import views

urlpatterns = [
    path('facilities/list', views.facility_get_list),
    path('facilities', views.facility_post_create),
    path('facilities/<int:facility_id>/', views.facility_get_by_id),
    path('facilities/<int:facility_id>/update', views.facility_put),
    path('facilities/<int:facility_id>/delete', views.facility_delete)
]