"""Módulo para requisições à API do painel"""

import pandas as pd
import requests
from callbacks.utils import get_code_regiao, get_ibge_code

API_URL = "https://dash-saude-mongo.elsvital.dev/api/v1"


def make_request(url):
    """Função para fazer uma requisição à API"""
    headers = {"accept": "application/json"}

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
    print("Fazendo request para:", url)

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


def get_anos(num):
    """Retorna uma lista com os anos a serem utilizados"""
    url = f"{API_URL}/years"

    anos = make_request(url)
    anos = anos[-num:]
    anos.sort(reverse=True)

    return anos