from .connection import db


def get_cities_by_state(state):
    """
    Função para obter uma lista de municípios únicos associados a uma UF.

    :param state: Sigla do estado (UF).
    :return: Lista de municípios pertencentes à UF.
    """
    collection = db["cities"]  # Nome da sua coleção
    cities = collection.distinct('cidade', {'uf': state})  # Filtra pela UF
    return list(cities)
