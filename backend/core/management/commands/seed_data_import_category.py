import os, json
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models.data_import import DataImportCategory


class Command(BaseCommand):
    help = 'Import DataImportCategorys from an Excel file'

    def handle(self, *args, **kwargs):

        json_node_name = "data_import_category"
        json_file_path = os.path.join(settings.BASE_DIR, 'core', 'management', 'commands', 'seed_json',
                                      f'{json_node_name}.json')
        # Carregar os dados JSON
        with open(json_file_path, 'r') as json_file:
            data_class = json.load(json_file)

        for attribute_name, attribute_data in data_class[json_node_name].items():
            if DataImportCategory.objects.filter(name=attribute_name).exists():
                self.stdout.write(self.style.WARNING(
                    f"DataImportCategorys with name {attribute_name} already exists. Skipping."))
                continue

            import_category = DataImportCategory.objects.create(
                name=attribute_name,
                description=attribute_data['description'],
            )
            self.stdout.write(self.style.SUCCESS(f"Imported DataImportCategorys {import_category.name}"))
