from config.global_vars import IGNORE_KEYS
from database.collections import get_collection_attributes
from database.connection import db


def aggregation_collections(collection_name, aggregation_field, state_match_list=None, year_match_list=None):
    # Lista de colunas que você deseja agrupar e somar
    columns_to_group = aggregation_field  # Agrupar por "Uf" e "region"
    ignore_keys = IGNORE_KEYS
    # columns_to_sum = ["value1", "value2", "value3"]  # Colunas cujos valores serão somados
    columns_to_sum = []
    collection = db[collection_name]
    header = collection.find().limit(1)
    for document in header:
        for key, value in document.items():
            if key not in ignore_keys:
                if key != '_id':
                    columns_to_sum.append(key)

    # Criando o estágio $group dinamicamente
    group_stage = {
        "_id": {}  # A chave "_id" define como os documentos serão agrupados
    }

    # Preencher o "_id" com as colunas da lista 'columns_to_group'
    for column in columns_to_group:
        group_stage["_id"][column] = f"${column}"  # Definir dinamicamente cada coluna no agrupamento

    # Adicionar dinamicamente as somas para as colunas da lista 'columns_to_sum'
    for column in columns_to_sum:
        group_stage[f"{column}"] = {"$sum": f"${column}"}

    # Definir o pipeline de agregação com o estágio $group dinâmico

    if state_match_list and year_match_list:
        pipeline = [
            {"$match": {"Uf": {"$in": state_match_list}, "Ano": {"$in": year_match_list}}},
            # Um exemplo de filtro, opcional
            {"$group": group_stage}
        ]
    elif state_match_list and not year_match_list:
        pipeline = [
            {"$match": {"Uf": {"$in": state_match_list}}},  # Um exemplo de filtro, opcional
            {"$group": group_stage}
        ]
    elif not state_match_list and year_match_list:
        pipeline = [
            {"$match": {"Ano": {"$in": year_match_list}}},  # Um exemplo de filtro, opcional
            {"$group": group_stage}
        ]
    else:
        pipeline = [
            {"$group": group_stage}
        ]

    # Executar a agregação
    result = list(collection.aggregate(pipeline))
    return result


def aggregation_by(collection_name, aggregation_field, regions=None, states=None, cities=None):
    # Lista de colunas que você deseja agrupar e somar
    columns_to_group = aggregation_field  # Agrupar por "Uf" e "region"
    ignore_keys = IGNORE_KEYS
    # columns_to_sum = ["value1", "value2", "value3"]  # Colunas cujos valores serão somados
    columns_to_sum = []
    collection = db[collection_name]
    attributes = get_collection_attributes(collection_name)
    for attribute in attributes:
        columns_to_sum.append(attribute)

    # Criando o estágio $group dinamicamente
    group_stage = {
        "_id": {}  # A chave "_id" define como os documentos serão agrupados
    }

    # Preencher o "_id" com as colunas da lista 'columns_to_group'
    for column in columns_to_group:
        group_stage["_id"][column] = f"${column}"  # Definir dinamicamente cada coluna no agrupamento

    # Adicionar dinamicamente as somas para as colunas da lista 'columns_to_sum'
    for column in columns_to_sum:
        # {"$toInt": "$Complementado"},
        group_stage[f"{column}"] = {"$sum": f"${column}"}

    # Definir o pipeline de agregação com o estágio $group dinâmico

    if states:
        pipeline = [
            {"$match": {"Uf": {"$in": states}}},
            # Um exemplo de filtro, opcional
            {"$group": group_stage}
        ]
    elif regions:
        pipeline = [
            {"$match": {"region": {"$in": regions}}},
            # Um exemplo de filtro, opcional
            {"$group": group_stage}
        ]
    elif cities:
        pipeline = [
            {"$match": {"Ibge": {"$in": cities}}},
            # Um exemplo de filtro, opcional
            {"$group": group_stage}
        ]
    else:
        pipeline = [
            {"$group": group_stage}
        ]

    # Executar a agregação
    result = list(collection.aggregate(pipeline))
    return result
