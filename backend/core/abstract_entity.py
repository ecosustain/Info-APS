from django.db import models


class AuditableEntity(models.Model):
    """
    This class represents an abstract model called AuditableEntity. It provides fields and methods related to auditing and ownership of an entity.

    Attributes:
        - created_at (DateTimeField): Represents the date and time when the entity was created.
        - updated_at (DateTimeField): Represents the date and time when the entity was last updated.
    Meta:
        - abstract (boolean): Indicates that this model should not be created as a separate table in the database.

    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update date")

    class Meta:
        abstract = True  # não crie uma tabela no banco de dados.


class Category(AuditableEntity):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class HealthCore(AuditableEntity):
    group_param = models.CharField(max_length=255, null=False, blank=False)
    class_param = models.CharField(max_length=255, null=False, blank=False)
    ine = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=False, blank=False)
    month = models.IntegerField(null=False, blank=False)

    class Meta:
        abstract = True  # não crie uma tabela no banco de dados

    def __str__(self):
        return f'{self.group_param} - {self.class_param}'


class HealthCoreCategory(models.Model):
    value = models.IntegerField(null=False, blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.value}'
