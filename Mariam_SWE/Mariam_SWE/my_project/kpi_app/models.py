from django.db import models

# Create your models here.

class KPI(models.Model):
    name = models.CharField(max_length=100)
    expression = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class KPIAssetLink(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name="assets")
    asset_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.kpi_app.name} - {self.asset_id}"
