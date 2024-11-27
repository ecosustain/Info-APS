from helpers.aggregation import aggregation_collections
from helpers.collections import get_all_collections

from .connection import db


def get_collection_sum_states(states):
    total_sum = {}
    for state in states:
        total_sum[state] = {}

    for state in states:
        for collection_name in get_all_collections():
            partial_collection_sum = aggregation_collections(
                collection_name, ["Uf"], [state]
            )
            total_sum[state][collection_name] = partial_collection_sum

    return total_sum


def get_collection_sum_states_year(states, years):
    total_sum = {}
    for state in states:
        total_sum[state] = {}

    for state in states:
        for collection_name in get_all_collections():
            partial_collection_sum = aggregation_collections(
                collection_name, ["Uf", "Ano"], [state], [years]
            )
            total_sum[state][collection_name] = partial_collection_sum

    return total_sum


def get_state():
    """
    Função para obter uma lista de UFs únicas em uma coleção.

    :param collection_name: Nome da coleção no MongoDB.
    :return: Lista de UFs distintas.
    """
    collection = db["states"]
    states = collection.find({}, {"_id": 0, "name": 1, "description": 1})
    return [state["name"] for state in states]
