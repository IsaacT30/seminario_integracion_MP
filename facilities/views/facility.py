from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import MedicalFacility
from ..serializers import MedicalFacilitySerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def facility_get_list(request):
    qs = MedicalFacility.objects.all()
    q = (request.query_params.get("q") or "").strip()
    facility_type = request.query_params.get("facility_type")
    
    if q:
        qs = qs.filter(Q(code__icontains=q) |
                       Q(name__icontains=q) |
                       Q(city__icontains=q))
    if facility_type:
        qs = qs.filter(facility_type=facility_type)
    
    data = MedicalFacilitySerializer(qs, many=True).data
    return Response(data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def facility_post_create(request):
    serializer = MedicalFacilitySerializer(data=request.data)
    if serializer.is_valid():
        facility = serializer.save()
        return Response(MedicalFacilitySerializer(facility).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def facility_get_by_id(request, facility_id: int):
    try:
        facility = MedicalFacility.objects.get(pk=facility_id)
    except MedicalFacility.DoesNotExist:
        return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(MedicalFacilitySerializer(facility).data, status=status.HTTP_200_OK)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def facility_put(request, facility_id: int):
    try:
        facility = MedicalFacility.objects.get(pk=facility_id)
    except MedicalFacility.DoesNotExist:
        return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MedicalFacilitySerializer(facility, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def facility_delete(request, facility_id: int):
    try:
        facility = MedicalFacility.objects.get(pk=facility_id)
    except MedicalFacility.DoesNotExist:
        return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    facility.delete()
    return Response({'detail': 'Registro eliminado'}, status=status.HTTP_200_OK)