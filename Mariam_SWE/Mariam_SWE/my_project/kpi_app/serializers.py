from rest_framework import serializers
from .models import KPI, KPIAssetLink

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ['id', 'name', 'expression', 'description']

class KPIAssetLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIAssetLink
        fields = ['id', 'kpi', 'asset_id']
