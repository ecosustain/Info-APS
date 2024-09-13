import pandas as pd
from django.db import transaction
from core.models.geo_unit import GeoUnit
from unidecode import unidecode
from django.core.management.base import BaseCommand


# Função para formatar o nome do município e UF
def format_name(name):
    if pd.notnull(name):
        # Remove acentos e transforma em lowercase
        return unidecode(str(name)).strip().lower()
    return ''


# Função para normalizar o nome removendo acentos e convertendo para lowercase
def normalize_name(name):
    if pd.notnull(name):
        return unidecode(str(name)).strip().lower()
    return ''


class Command(BaseCommand):
    help = 'Seeds Actions.'

    def handle(self, *args, **options):
        # Carrega o arquivo Excel com os dados dos municípios
        excel_file = '~/sisab-data-dist/landing/MunicipiosBrasil.xlsx'  # Caminho do arquivo
        df = pd.read_excel(excel_file, engine='openpyxl')

        updated_count = 0
        with transaction.atomic():  # Usa transações para garantir consistência
            for index, row in df.iterrows():
                municipio_excel = normalize_name(row['MUNICIPIO'])
                uf_excel = normalize_name(row['UF'])
                latitude = row['LATITUDE']
                longitude = row['LONGITUDE']

                # Busca todos os GeoUnits e normaliza os nomes para comparação
                geo_units = GeoUnit.objects.filter(parent__name__iexact=row['UF'])  # Filtra primeiro pela UF

                for geo_unit in geo_units:
                    # Normaliza o nome do município no banco para comparação
                    normalized_name = normalize_name(geo_unit.name)
                    if normalized_name == municipio_excel:
                        # Atualiza a latitude e longitude mantendo o nome original acentuado
                        geo_unit.latitude = latitude
                        geo_unit.longitude = longitude
                        geo_unit.save()
                        updated_count += 1
                        break  # Para a iteração após encontrar a correspondência
                else:
                    print(
                        f'Não econtrado: {updated_count}/{len(df)}: {municipio_excel} - {uf_excel} - {latitude}, {longitude}')

        print(f'{updated_count} registros atualizados com sucesso.')
