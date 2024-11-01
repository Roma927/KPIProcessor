from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import KPI, KPIAssetLink
from .serializers import KPISerializer, KPIAssetLinkSerializer
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status
from django.http import HttpResponse

# kpi_app/views.py

@api_view(['POST'])
def create_kpi(request):
    # Handle the request and return a response
    name = request.data.get("name")
    expression = request.data.get("expression")
    description = request.data.get("description")
    # Process and store the KPI, then respond
    return Response({"message": "KPI created successfully", "data": {"name": name, "expression": expression, "description": description}})


class KPIViewSet(viewsets.ModelViewSet):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer

class KPIAssetLinkViewSet(viewsets.ModelViewSet):
    queryset = KPIAssetLink.objects.all()
    serializer_class = KPIAssetLinkSerializer

    @action(detail=True, methods=['post'])
    def link_asset(self, request, pk=None):
        kpi = self.get_object()
        asset_id = request.data.get('asset_id')
        if asset_id:
            kpi_asset_link, created = KPIAssetLink.objects.get_or_create(kpi=kpi, asset_id=asset_id)
            serializer = KPIAssetLinkSerializer(kpi_asset_link)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response({'error': 'Asset ID is required'}, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return HttpResponse("Welcome to the KPI, Go to /swagger/ for API documentation;)")
