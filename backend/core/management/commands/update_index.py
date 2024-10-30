import pandas as pd
from core.models.geo_unit import GeoUnit
from core.models.individual_care import IndividualCare
from django.core.management.base import BaseCommand
from django.db import transaction
from pip._vendor.rich.region import Region
from unidecode import unidecode


# Função para formatar o nome do município e UF
def format_name(name):
    if pd.notnull(name):
        # Remove acentos e transforma em lowercase
        return unidecode(str(name)).strip().lower()
    return ""


# Função para normalizar o nome removendo acentos e convertendo para lowercase
def normalize_name(name):
    if pd.notnull(name):
        return unidecode(str(name)).strip().lower()
    return ""


class Command(BaseCommand):
    help = "Seeds Actions."

    def handle(self, *args, **options):
        individual_cares = IndividualCare.objects.all()
        total_count = individual_cares.count()
        count = 0
        for reg in individual_cares:
            print(reg.geo_unit.name)
            count += 1
            print(f"{count} of {total_count}")
            reg.geo_unit_state = reg.geo_unit.parent
            reg.geo_unit_macro_region = reg.geo_unit.parent.parent
            reg.save()
