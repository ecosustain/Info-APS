from django.db import models
from core.abstract_entity import AuditableEntity


class GeoUnitType(AuditableEntity):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = 'geo_unit_type'

    def __str__(self):
        return self.name


class GeoUnit(AuditableEntity):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(GeoUnitType, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    ibge = models.IntegerField(null=True, blank=True)
    cnes = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'geo_unit'
        indexes = [
            models.Index(fields=['name'], name='geo_unit_name_index'),
        ]
        unique_together = (('name', 'parent'),)  # Define a combinação única de name e parent

    def __str__(self):
        return self.name
