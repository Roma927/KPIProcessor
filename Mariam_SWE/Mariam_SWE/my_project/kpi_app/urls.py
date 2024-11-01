from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KPIViewSet, KPIAssetLinkViewSet

router = DefaultRouter()
router.register('kpis', KPIViewSet, basename='KPIS')
router.register('kpi-assets', KPIAssetLinkViewSet, basename='assetKPI')

urlpatterns = [
    path('', include(router.urls)),
]
