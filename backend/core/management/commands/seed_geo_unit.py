import os, json
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models.geo_unit import GeoUnit, GeoUnitType


class Command(BaseCommand):
    help = 'Seeds Actions.'

    def handle(self, *args, **options):
        json_node_name = "geo_unit"

        json_file_path = os.path.join(settings.BASE_DIR, 'core', 'management', 'commands', 'seed_json',
                                      f'{json_node_name}.json')
        # Carregar os dados JSON
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Criar os tipos de unidades geográficas, se ainda não existirem
        country_type, _ = GeoUnitType.objects.get_or_create(name="Pais")
        macro_region_type, _ = GeoUnitType.objects.get_or_create(name="Macro-Regiao")
        state_type, _ = GeoUnitType.objects.get_or_create(name="Estado")
        count_type, _ = GeoUnitType.objects.get_or_create(name="Municipio")

        # Loop sobre cada país no JSON
        for pais in data["paises"]:
            # Criar ou obter o país
            pais_obj, _ = GeoUnit.objects.get_or_create(
                name=pais["nome"],
                description=f"{pais['nome']}",
                type=country_type,
                parent=None
            )

            # Loop sobre as macro-regiões do país
            for macro_regiao in pais.get("macro_regioes", []):
                # Criar ou obter a macro-região associada ao país
                macro_regiao_obj, _ = GeoUnit.objects.get_or_create(
                    name=macro_regiao["nome"],
                    description=f"{macro_regiao['nome']}",
                    type=macro_region_type,
                    parent=pais_obj
                )

                # Loop sobre os estados da macro-região
                for estado in macro_regiao.get("estados", []):
                    # Criar ou obter o estado associado à macro-região
                    estado_arr = estado.split(",")
                    GeoUnit.objects.get_or_create(
                        name=estado_arr[0],
                        description=f"{estado_arr[1]}.",
                        type=state_type,
                        parent=macro_regiao_obj
                    )
