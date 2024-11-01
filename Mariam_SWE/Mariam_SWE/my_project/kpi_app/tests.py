from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import KPI, KPIAssetLink

class KPITests(APITestCase):
    def test_create_kpi(self):
        url = reverse('kpi-list')
        data = {'name': 'Test KPI', 'expression': 'ATTR + 10', 'description': 'Test KPI description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_link_asset_to_kpi(self):
        kpi = KPI.objects.create(name='Test KPI', expression='ATTR + 10')
        url = reverse('kpiassetlink-list')
        data = {'kpi': kpi.id, 'asset_id': 'asset123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

