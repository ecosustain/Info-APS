import csv
import os
from database.connection import db
from helpers.collections import get_all_collections

from apis.files import set_progress, start_progress


def count_csv_records(file_path):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        # Converter em uma lista e contar os elementos
        records = list(reader)
    return len(records)


def process_csv_file(file, collection_name):
    """
    Função para processar o arquivo CSV e inserir os dados na coleção MongoDB.
    Converte valores numéricos que estão como strings para inteiros, remove .0 e ignora valores zero (0).

    :param file: Arquivo CSV
    :param collection_name: Nome da coleção MongoDB
    """
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Converter cada linha do CSV em um documento MongoDB
    total_records = count_csv_records(file_path)
    step = 0
    # Atualizar o total de registros no progresso
    start_progress(total_records)

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        collection = db[collection_name]
        # cities = db['cities']

        for row in reader:
            document = {}
            for key, value in row.items():
                if value is not None:
                    value = value.strip()  # Remove espaços extras
                key = key.strip().replace(".", "")
                # Verifica se o valor termina com .0 (como 2024.0) e remove o .0
                if value.endswith(".0"):
                    value = value[
                        :-2
                    ]  # Remove os últimos dois caracteres (".0")

                if value is not None:
                    value = value.strip().replace(
                        ".", ""
                    )  # Remove espaços extras

                # Verificar se o valor é uma string com números e remover pontos
                if value.replace(".", "", 1).isdigit():
                    try:
                        # Converte para inteiro após remover pontos de milhar
                        int_value = int(value.replace(".", ""))
                        # Ignora valores zero
                        if int_value != 0:
                            document[key] = int_value
                    except ValueError:
                        # Se não for possível converter para inteiro, mantenha o valor original
                        document[key] = value
                else:
                    # Se não for um número, insere como string
                    document[key] = value

            set_progress(step + 1, int(((step + 1) / total_records) * 100))
            step += 1

            # Se houver algum valor no documento, insere no MongoDB
            if (
                document
            ):  # Certifica que não estamos inserindo um documento vazio
                collection.insert_one(document)

    set_progress(step + 1, 100)


def update_collection_attributes(collection_name, based_on_first=None):
    # Obter a coleção onde os documentos estão
    collection = db[collection_name]
    if based_on_first:
        documents = [collection.find_one()]
    else:
        documents = collection.find()

    # Usar um set para evitar duplicatas
    attributes_set = set()

    # Iterar sobre todos os documentos da coleção e coletar os atributos (chaves)
    for document in documents:
        for key in document.keys():
            # Adicionar o atributo à lista de atributos
            if key != "_id":  # Ignorar o campo '_id'
                attributes_set.add(key)

    # Converter o set para uma lista ordenada
    attributes_list = sorted(list(attributes_set))

    # Inserir ou atualizar os atributos na coleção 'collection_attributes'
    db["collection_attributes"].update_one(
        {"collection": collection_name},  # Filtro para a coleção específica
        {
            "$set": {"attributes": attributes_list}
        },  # Atualização da lista de atributos
        upsert=True,  # Insere um novo documento se não encontrar a coleção
    )

    return attributes_list


def update_collections_attributes(collection_name=None, based_on_first=None):
    if collection_name:
        print(collection_name)
        attributes_list = update_collection_attributes(
            collection_name, based_on_first
        )
        print(attributes_list)
    else:
        collections = get_all_collections()
        for collection_name in collections:
            print(collection_name)
            attributes_list = update_collection_attributes(
                collection_name, based_on_first
            )
            print(attributes_list)


def is_collection_empty(collection_name):
    collection = db[collection_name]
    # Tenta encontrar um documento
    document = collection.find_one()
    return (
        document is None
    )  # Retorna True se não encontrar documento, indicando que está vazia
