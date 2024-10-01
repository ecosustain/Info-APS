import json
import os

from core.models.data_import import (
    DataImportCategory,
    DataImportParam,
    DataImportProfile,
)
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import DataImportProfiles from an Excel file"

    def handle(self, *args, **kwargs):
        DataImportParam.objects.all().delete()
        DataImportProfile.objects.all().delete()

        json_node_name = "data_import_profile"
        json_file_path = os.path.join(
            settings.BASE_DIR,
            "core",
            "management",
            "commands",
            "seed_json",
            f"{json_node_name}.json",
        )
        with open(json_file_path, "r") as json_file:
            data_class = json.load(json_file)

        data_import_category = DataImportCategory.objects.get(
            name="import_data_file"
        )

        for attribute_name, attribute_data in data_class[
            json_node_name
        ].items():
            if DataImportProfile.objects.filter(name=attribute_name).exists():
                data_import_profile = DataImportProfile.objects.get(
                    name=attribute_name
                )
                self.stdout.write(
                    self.style.WARNING(
                        f"DataImportProfiles with name {attribute_name} already exists. Skipping."
                    )
                )
            else:
                data_import_profile = DataImportProfile.objects.create(
                    name=attribute_name,
                    description=attribute_data["description"],
                    data_import_category=data_import_category,
                )

            if data_import_profile:
                for params in attribute_data["params"]:
                    extra_data = {str(k): str(v) for k, v in params.items()}
                    (
                        data_import_param,
                        created,
                    ) = DataImportParam.objects.get_or_create(
                        name="file_import_param",
                        value=extra_data,
                        data_import_profile=data_import_profile,
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Imported DataImportProfiles {data_import_profile.name}"
                )
            )
