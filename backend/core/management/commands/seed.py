from django.core.management.base import BaseCommand
from core.models.data_import import DataImportProfile, DataImportLog
import os
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from django.core.management import call_command


def move_and_rename_file(file_name):
    # Extrai o caminho da pasta de origem a partir do caminho completo do arquivo
    source_folder = os.path.dirname(file_name)

    # Volta um nível no diretório e concatena com 'processed' para definir a pasta de destino
    parent_folder = os.path.dirname(source_folder)
    destination_folder = os.path.join(parent_folder, 'processed')

    # Verifica se o arquivo existe na pasta de origem
    if not os.path.exists(file_name):
        print(f"Arquivo {file_name} não encontrado.")
        return

    # Cria a pasta de destino se ela não existir
    os.makedirs(destination_folder, exist_ok=True)

    # Gerando o timestamp para adicionar ao nome do arquivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Novo nome do arquivo com o timestamp
    file_name_with_timestamp = f"{os.path.splitext(os.path.basename(file_name))[0]}_{timestamp}{os.path.splitext(file_name)[1]}"

    # Caminho completo do arquivo na pasta de destino
    destination_path = os.path.join(destination_folder, file_name_with_timestamp)

    # Movendo e renomeando o arquivo
    try:
        shutil.move(file_name, destination_path)
        print(f"Arquivo movido com sucesso para {destination_folder} com o nome {file_name_with_timestamp}.")
    except Exception as e:
        print(f"Erro ao mover o arquivo: {e}")


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        call_command('seed_geo_unit')
        call_command('seed_data_import_category')
        call_command('seed_data_import_profle')

        data_import_profiles = DataImportProfile.objects.get(data_import_category_id='import_data_file', active=True)
        run_import(data_import_profiles)

        # Atualiza lat, lon
        # call_command('import_city_location')
        # call_command('import_state_location')


def process_file(param, data_import_profiles):
    file_path = param.value['file_name']
    group_param = param.value['group_param']
    class_param = param.value['class_param']

    if os.path.isfile(file_path):
        try:
            print(f"Processing File Name: {file_path}, Group: {group_param}")
            call_command('import_raw_data', group_param, class_param, file_path)
            DataImportLog.objects.create(
                data_import_profile=data_import_profiles,
                status='Success',
                file_name=file_path
            )
            # Move o arquivo para processados
            move_and_rename_file(file_path)

        except Exception as e:
            print(f'Error: {e}')
            DataImportLog.objects.create(
                data_import_profile=data_import_profiles,
                status='Error',
                message=str(e),
                file_name=file_path
            )
    else:
        error = f"O arquivo {file_path} não foi encontrado."
        print(error)
        DataImportLog.objects.create(
            data_import_profile=data_import_profiles,
            status='Error',
            message=error,
            file_name=file_path
        )


def run_import(data_import_profiles):
    active_params = data_import_profiles.params.filter(active=True, name='file_import_param')

    with ThreadPoolExecutor() as executor:
        for param in active_params:
            executor.submit(process_file, param, data_import_profiles)
    print('Data seeded successfully!')
