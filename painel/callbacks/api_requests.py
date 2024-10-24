"""Módulo para requisições à API do painel"""

import pandas as pd
import requests
from callbacks.utils import get_code_regiao, get_ibge_code


def get_municipios(estado):
    """Função para obter os municipios de um estado"""
    url = f"https://dash-saude-mongo.elsvital.dev/api/v1/cities/{estado}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        cities = response.json()
        return cities
    else:
        print(response.status_code)
        print(response.text)
        return None


def get_atendimentos(estado, regiao, municipio):
    """Função para obter os dados de atendimentos"""
    url = "https://dash-saude-mongo.elsvital.dev/api/v1/atendimentos"
    if estado is not None:
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/atendimentos/states/{estado}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/atendimentos/regions/{regiao_code}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/atendimentos/cities/{ibge_code}"
    print("Fazendo request para:", url)

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.text)
        return None


def get_altas(estado, regiao, municipio):
    """Função para obter os dados de altas"""
    url = "https://dash-saude-mongo.elsvital.dev/api/v1/altas"
    if estado is not None:
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/altas/states/{estado}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/altas/regions/{regiao_code}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/altas/cities/{ibge_code}"
    print("Fazendo request para:", url)
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.text)
        return None


def get_encaminhamentos(estado, regiao, municipio):
    """Função para obter os dados de encaminhamentos"""
    url = "https://dash-saude-mongo.elsvital.dev/api/v1/encaminhamentos"
    if estado is not None:
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/encaminhamentos/states/{estado}"
    if regiao is not None and estado is not None and municipio is None:
        regiao_code = get_code_regiao(estado, regiao)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/encaminhamentos/regions/{regiao_code}"
    if municipio is not None and estado is not None:
        ibge_code = get_ibge_code(estado, municipio)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/encaminhamentos/cities/{ibge_code}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.text)
        return None


def get_anos(num):
    """Retorna uma lista com os anos a serem utilizados"""
    url = f"https://dash-saude-mongo.elsvital.dev/api/v1/years"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        anos = response.json()
        anos = anos[-num:]
        anos.sort(reverse=True)
        return anos
    else:
        print(response.status_code)
        print(response.text)
        return None
