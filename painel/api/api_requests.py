"""Módulo para requisições à API do painel"""

import requests
from callbacks.utils.utils import get_code_regiao, get_ibge_code

API_URL = "https://dash-saude-mongo.elsvital.dev/api/v1"


def make_request(url):
    """Função para fazer uma requisição à API"""
    headers = {"accept": "application/json"}
    print("Fazendo request para:", url)
    response = requests.get(url, headers=headers, timeout=20)

    if response.status_code == 200:
        return response.json()

    print(response.status_code)
    print(response.text)
    return None


def get_municipios(estado):
    """Função para obter os municipios de um estado"""
    url = f"{API_URL}/cities/{estado}"

    return make_request(url)


def get_atendimentos(estado, regiao, municipio):
    """Função para obter os dados de atendimentos"""
    if municipio:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/atendimentos/cities/{ibge_code}"
    elif regiao:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/atendimentos/regions/{regiao_code}"
    elif estado:
        url = f"{API_URL}/atendimentos/states/{estado}"
    else:
        url = f"{API_URL}/atendimentos"

    return make_request(url)


def get_visitas_domiciliar(estado, regiao, municipio):
    """Função para obter os dados de visitas_domiciliar"""
    if municipio:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/visitas_domiciliar/cities/{ibge_code}"
    elif regiao:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/visitas_domiciliar/regions/{regiao_code}"
    elif estado:
        url = f"{API_URL}/visitas_domiciliar/states/{estado}"
    else:
        url = f"{API_URL}/visitas_domiciliar"

    return make_request(url)


def get_atendimentos_odontologicos(estado, regiao, municipio):
    """Função para obter os dados de atendimentos_odontologicos"""
    if municipio:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/atendimentos_odontologicos/cities/{ibge_code}"
    elif regiao:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/atendimentos_odontologicos/regions/{regiao_code}"
    elif estado:
        url = f"{API_URL}/atendimentos_odontologicos/states/{estado}"
    else:
        url = f"{API_URL}/atendimentos_odontologicos"

    return make_request(url)


def get_encaminhamentos(estado, regiao, municipio):
    """Função para obter os dados de encaminhamentos"""
    if municipio:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/encaminhamentos/cities/{ibge_code}"
    elif regiao:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/encaminhamentos/regions/{regiao_code}"
    elif estado:
        url = f"{API_URL}/encaminhamentos/states/{estado}"
    else:
        url = f"{API_URL}/encaminhamentos"

    return make_request(url)


def get_atendimentos_individuais_problema(estado, regiao, municipio, problema):
    """Função para obter os dados de atendimento inidividual por problema de saúde"""
    if municipio:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/atendimento_individual/cities/{ibge_code}/{problema}"
    elif regiao:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/atendimento_individual/regions/{regiao_code}/{problema}"
    elif estado:
        url = f"{API_URL}/atendimento_individual/states/{estado}/{problema}"
    else:
        url = f"{API_URL}/atendimento_individual/{problema}"

    return make_request(url)


def get_collection(estado, regiao, municipio, collection, colunas):
    """Função para obter os dados de uma coleção específica"""
    if municipio:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/{collection}/cities/{ibge_code}/{colunas}"
    elif regiao:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/{collection}/regions/{regiao_code}/{colunas}"
    elif estado:
        url = f"{API_URL}/{collection}/states/{estado}/{colunas}"
    else:
        url = f"{API_URL}/{collection}/{colunas}"

    return make_request(url)


def get_anos(num):
    """Retorna uma lista com os anos a serem utilizados"""
    url = f"{API_URL}/years"

    anos_api = make_request(url)
    anos_api = anos_api[-num:]
    anos_api.sort(reverse=True)

    return anos_api


anos = get_anos(6)


def get_collection_atributes(collection):
    """Função para obter os atributos de uma coleção"""
    url = f"{API_URL}/collections/{collection}/attributes"

    return make_request(url)


def get_febres(estado, regiao, municipio):
    """Função para obter as palavras relacionadas à febre"""
    if municipio:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"{API_URL}/cids_febre/cities/{ibge_code}"
    elif regiao:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"{API_URL}/cids_febre/regions/{regiao_code}"
    elif estado:
        url = f"{API_URL}/cids_febre/states/{estado}"
    else:
        url = f"{API_URL}/cids_febre"

    return make_request(url)
