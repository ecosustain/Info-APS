from django.contrib.postgres.fields import HStoreField
from django.db import models
from core.abstract_entity import AuditableEntity


class DataImportCategory(AuditableEntity):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = 'data_import_category'

    def __str__(self):
        return self.name


class DataImportProfile(AuditableEntity):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)
    data_import_category = models.ForeignKey(DataImportCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'data_import_profile'

    def __str__(self):
        return self.name


class DataImportParam(AuditableEntity):
    name = models.CharField(max_length=100)
    value = HStoreField(null=True, blank=True)  # Adiciona o campo HStore
    data_import_profile = models.ForeignKey(DataImportProfile, on_delete=models.CASCADE, related_name='params')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'data_import_param'


class DataImportLog(models.Model):
    # Log das importações realizadas
    data_import_profile = models.ForeignKey(DataImportProfile, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, null=False, blank=False)  # Nome do arquivo importado
    import_date = models.DateTimeField(auto_now_add=True)  # Data e hora da importação
    status = models.CharField(max_length=50, choices=[('SUCCESS', 'Success'), ('ERROR', 'Error')], default='SUCCESS')
    message = models.TextField(null=True, blank=True)  # Mensagem de erro ou informação adicional

    def __str__(self):
        return f"{self.file_name} - {self.get_status_display()}"

    class Meta:
        db_table = 'data_import_log'
