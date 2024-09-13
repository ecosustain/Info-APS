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
    geo_unit = models.ForeignKey(GeoUnit, on_delete=models.CASCADE)
    individual_category = models.ManyToManyField(IndividualCategory, through='IndividualCareCategory')

    class Meta:
        db_table = 'individual_care'
        indexes = [
            models.Index(fields=['year'], name='index_year'),
            models.Index(fields=['year', 'month'], name='index_year_month'),
        ]


class IndividualCareCategory(HealthCoreCategory):
    individual_care = models.ForeignKey(IndividualCare, on_delete=models.CASCADE)
    individual_category = models.ForeignKey(IndividualCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'individual_care_category'
        # Criar um índice único combinando os dois campos
        constraints = [
            models.UniqueConstraint(
                fields=['individual_care', 'individual_category'],
                name='unique_individual_care_category'
            )
        ]
