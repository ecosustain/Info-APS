import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models.individual_care import IndividualCare, IndividualCareCategory, IndividualCategory
from core.models.geo_unit import GeoUnit, GeoUnitType


def mes_para_numero(mes_sigla):
    # Dicionário mapeando siglas dos meses para seus valores numéricos
    meses = {
        "JAN": 1,
        "FEV": 2,
        "MAR": 3,
        "ABR": 4,
        "MAI": 5,
        "JUN": 6,
        "JUL": 7,
        "AGO": 8,
        "SET": 9,
        "OUT": 10,
        "NOV": 11,
        "DEZ": 12
    }
    # Converte a sigla para maiúscula para garantir correspondência correta
    return meses.get(mes_sigla.upper(), "Mês inválido")


def add_or_get_category(name):
    try:
        # Tenta obter a categoria pela chave única que está causando o erro
        category, created = IndividualCategory.objects.get_or_create(
            name=name
        )
        if created:
            print(f"Categoria '{name}' criada com sucesso.")
        else:
            print(f"Categoria '{name}' já existe e foi selecionada.")

    except Exception as e:
        # Caso o objeto já exista com o mesmo 'name', mas outros atributos diferentes
        print(f"Categoria '{name}' já existe. Usando a categoria existente. {e}")
        category = IndividualCategory.objects.get(name=name)

    return category


def load_data(file_path):
    # Verifica a extensão do arquivo
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        # Carrega arquivos Excel
        df = pd.read_excel(file_path, engine='openpyxl')
    elif file_path.endswith('.csv'):
        # Carrega arquivos CSV
        df = pd.read_csv(file_path, delimiter=',', low_memory=False)  # Assumindo que o separador é uma vírgula
    else:
        raise ValueError("Formato de arquivo não suportado. Use .xlsx, .xls ou .csv")

    return df


class Command(BaseCommand):
    help = 'Import Raw Data from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('group_param', type=str, help='Group parameter.')
        parser.add_argument('class_param', type=str, help='Class parameter.')
        parser.add_argument('file_path', type=str, help='The Excel file path.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        group_param = kwargs['group_param']
        class_param = kwargs['class_param']

        df = load_data(file_path)
        df.replace(float('nan'), None, inplace=True)
        ignored_columns = ['Uf', 'Ibge', 'IBGE', 'CNES', 'Tipo Unidade', 'INE', 'Tipo Equipe', 'Municipio', 'Mes',
                           'Ano', 'Região']

        geo_unit_type = GeoUnitType.objects.get(name='Municipio')

        individual_category = {}
        for col in df.columns:
            if col not in ignored_columns:
                individual_category[col] = add_or_get_category(col.strip())

        for _, row in df.iterrows():
            parent = GeoUnit.objects.get(name=row["Uf"])
            year = int(row["Ano"])
            month = mes_para_numero(row["Mes"])
            city = row["Municipio"]
            ibge_code = int(row["Ibge"])
            try:
                with transaction.atomic():

                    geo_unit, created = GeoUnit.objects.get_or_create(
                        name=city,
                        type=geo_unit_type,
                        parent=parent,
                    )

                    if ibge_code:
                        geo_unit.ibge = ibge_code
                        geo_unit.save()

                    individual_care = IndividualCare.objects.create(group_param=group_param, class_param=class_param,
                                                                    geo_unit=geo_unit, year=year, month=month)
                    for col in df.columns:
                        if col not in ignored_columns and not pd.isna(row[col]):
                            if type(row[col]) == str:
                                value = int(row[col].replace(".", ""))
                            else:
                                value = int(row[col])
                            if not pd.isna(row[col]) and value != 0:
                                # Filtrando com base nos critérios de negócio
                                count = IndividualCare.objects.filter(
                                    group_param=group_param,
                                    class_param=class_param,
                                    year=year,
                                    month=month,
                                    geo_unit=geo_unit,
                                    individualcarecategory__individual_category__name=individual_category[col]
                                ).count()
                                if count == 0:
                                    IndividualCareCategory.objects.create(individual_care=individual_care,
                                                                          individual_category=individual_category[col],
                                                                          value=value)
                                else:
                                    raise Exception(
                                        f'Registro já importado: {individual_category[col]} => {value}. Ja gravado para {month}/{year}, {geo_unit.name}')
            except Exception as e:
                print(e)

        self.stdout.write(self.style.SUCCESS(f"Imported!"))
