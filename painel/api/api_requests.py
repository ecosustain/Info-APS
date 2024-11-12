"""Módulo para requisições à API do painel"""

import pandas as pd
import requests
from callbacks.utils.utils import get_code_regiao, get_ibge_code

API_URL = "https://dash-saude-mongo.elsvital.dev/api/v1"


def make_request(url):
    """Função para fazer uma requisição à API"""
    headers = {"accept": "application/json"}
    print("Fazendo request para:", url)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.text)
        return None


def get_municipios(estado):
    """Função para obter os municipios de um estado"""
    url = f"{API_URL}/cities/{estado}"

    return make_request(url)


def get_atendimentos(estado, regiao, municipio):
    """Função para obter os dados de atendimentos"""
    url = f"{API_URL}/atendimentos"
    if estado is not None:
        url = f"{API_URL}/atendimentos/states/{estado}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/atendimentos/regions/{regiao_code}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/atendimentos/cities/{ibge_code}"

    return make_request(url)


def get_visitas_domiciliar(estado, regiao, municipio):
    """Função para obter os dados de visitas_domiciliar"""
    url = f"{API_URL}/visitas_domiciliar"
    if estado is not None:
        url = f"{API_URL}/visitas_domiciliar/states/{estado}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/visitas_domiciliar/regions/{regiao_code}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/visitas_domiciliar/cities/{ibge_code}"

    return make_request(url)


def get_atendimentos_odontologicos(estado, regiao, municipio):
    """Função para obter os dados de atendimentos_odontologicos"""
    url = f"{API_URL}/atendimentos_odontologicos"
    if estado is not None:
        url = f"{API_URL}/atendimentos_odontologicos/states/{estado}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/atendimentos_odontologicos/regions/{regiao_code}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/atendimentos_odontologicos/cities/{ibge_code}"

    return make_request(url)


def get_encaminhamentos(estado, regiao, municipio):
    """Função para obter os dados de encaminhamentos"""
    url = f"{API_URL}/encaminhamentos"
    if estado is not None:
        url = f"{API_URL}/encaminhamentos/states/{estado}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/encaminhamentos/regions/{regiao_code}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/encaminhamentos/cities/{ibge_code}"

    return make_request(url)


def get_atendimentos_individuais_problema(estado, regiao, municipio, problema):
    """Função para obter os dados de atendimento inidividual por problema de saúde"""
    url = f"{API_URL}/atendimento_individual/{problema}"
    if estado is not None:
        url = f"{API_URL}/atendimento_individual/states/{estado}/{problema}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/atendimento_individual/regions/{regiao_code}/{problema}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/atendimento_individual/cities/{ibge_code}/{problema}"

    return make_request(url)


def get_collection(estado, regiao, municipio, collection, colunas):
    """Função para obter os dados de uma coleção específica"""
    url = f"{API_URL}/{collection}/{colunas}"
    if estado is not None:
        url = f"{API_URL}/{collection}/states/{estado}/{colunas}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/{collection}/regions/{regiao_code}/{colunas}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/{collection}/cities/{ibge_code}/{colunas}"

    return make_request(url)


def get_anos(num):
    """Retorna uma lista com os anos a serem utilizados"""
    url = f"{API_URL}/years"

    anos = make_request(url)
    anos = anos[-num:]
    anos.sort(reverse=True)

    return anos


anos = get_anos(6)


def get_collection_atributes(collection):
    """Função para obter os atributos de uma coleção"""
    url = f"{API_URL}/collections/{collection}/attributes"

    return make_request(url)


def get_febres(estado, regiao, municipio):
    """Função para obter as palavras relacionadas à febre"""
    url = f"{API_URL}/cids_febre"
    if estado is not None:
        url = f"{API_URL}/cids_febre/states/{estado}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/cids_febre/regions/{regiao_code}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/cids_febre/cities/{ibge_code}"

    return make_request(url)
