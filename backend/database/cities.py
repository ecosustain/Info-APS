from .connection import db


def get_cities_by_state(state):
    """
    Função para obter uma lista de municípios únicos associados a uma UF.

    :param state: Sigla do estado (UF).
    :return: Lista de municípios pertencentes à UF.
    """
    collection = db["cities"]  # Nome da sua coleção
    # cities = collection.distinct('cidade', {'uf': state})  # Filtra pela UF
    cities = collection.find({'uf': state}, {'_id': 1, 'cidade': 1})
    return list(cities)


def get_population(ibge, year, month):
    """
    Função para obter a população do município no Ano/Mês

    :param ibge: Código do IBGE.
    :param year: Ano.
    :param month: Mês.
    :return: Dicionário com total de habitantes cadastrados e nome do município no Ano/Mês, ou None se não encontrado.
    """
    collection = db["População"]  # Nome da sua coleção
    # Tenta encontrar o primeiro registro no filtro mais específico
    result = collection.find_one({'Ibge': ibge, 'Mes': month, 'Ano': year}, {'_id': 0, 'Cadastros': 1, 'Municipio': 1})

    # Caso não encontre, relaxa o filtro
    if result is None:
        result = collection.find_one({'Ibge': ibge, 'Ano': year}, {'_id': 0, 'Cadastros': 1, 'Municipio': 1})

    # Caso ainda não encontre, relaxa mais uma vez o filtro
    if result is None:
        result = collection.find_one({'Ibge': ibge}, {'_id': 0, 'Cadastros': 1, 'Municipio': 1})

    # Verifica se encontrou algum registro e retorna os valores de 'Cadastros' e 'Municipio'
    if result:
        cadastros = int(result.get('Cadastros', 0))  # Converte 'Cadastros' para inteiro
        municipio = result.get('Municipio', 'Não informado')
        return {'Cadastros': cadastros, 'Municipio': municipio}

    return None

