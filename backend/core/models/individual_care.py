from django.db import models
from core.abstract_entity import HealthCore, Category, HealthCoreCategory
from core.models.geo_unit import GeoUnit


class IndividualCategory(Category):
    class Meta:
        db_table = 'individual_category'
        indexes = [
            models.Index(fields=['name'], name='category_name_index'),
        ]


class IndividualCare(HealthCore):
    geo_unit_macro_region = models.ForeignKey(GeoUnit, on_delete=models.CASCADE, related_name='individual_care_geo_unit_macro_region')
    geo_unit_state = models.ForeignKey(GeoUnit, on_delete=models.CASCADE, related_name='individual_care_geo_unit_state')
    geo_unit = models.ForeignKey(GeoUnit, on_delete=models.CASCADE, related_name='individual_care_geo_unit')
    individual_category = models.ManyToManyField(IndividualCategory, through='IndividualCareCategory')

    class Meta:
        db_table = 'individual_care'
        indexes = [
            models.Index(fields=['geo_unit'], name='index_geo_unit'),
            models.Index(fields=['geo_unit_macro_region'], name='index_geo_unit_macro_region'),
            models.Index(fields=['geo_unit_state'], name='index_geo_unit_state'),
            models.Index(fields=['year'], name='index_year'),
            models.Index(fields=['month'], name='index_month'),
        ]


class IndividualCareCategory(HealthCoreCategory):
    individual_care = models.ForeignKey(IndividualCare, on_delete=models.CASCADE)
    individual_category = models.ForeignKey(IndividualCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'individual_care_category'
        # Criar um índice único combinando os dois campos
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['individual_care', 'individual_category'],
        #         name='unique_individual_care_category'
        #     )
        # ]
