"""Módulo para testar as requisicoes da API"""

import pytest

from painel.api import api_requests


def test_get_atendimentos_sp():
    """Testa a função get_atendimentos para SP"""
    result = api_requests.get_atendimentos("SP", None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert result['enfermeiro']['2023'] = 19927236
    assert result['médico']['2023'] = 50039489


def test_get_atendimentos_araras():
    """Testa a função get_atendimentos para Araras"""
    result = api_requests.get_atendimentos("SP", None, "ARARAS")
    assert result is not None, "Erro ao fazer a requisição"
    assert result['enfermeiro']['2023'] = 27305
    assert result['médico']['2023'] = 0


def test_get_atendimentos_adamantina():
    """Testa a função get_atendimentos para Adamantina"""
    result = api_requests.get_atendimentos("SP", "ADAMANTINA", None )
    assert result is not None, "Erro ao fazer a requisição"
    assert result['enfermeiro']['2023'] = 0
    assert result['médico']['2023'] = 0


def test_get_atendimentos_brasil():
    """Testa a função get_atendimentos para o Brasil"""
    result = api_requests.get_atendimentos(None, None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert result['enfermeiro']['2023'] = 0
    assert result['médico']['2023'] = 0


def test_get_visitas_brasil():
    """Testa a função get_visitas_domiciliar para o Brasil"""
    result = api_requests.get_visitas_domiciliar(None, None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert result['2023'] = 0
    assert result['2023'] = 0


def test_get_odonto_brasil():
    """Testa a função get_odontologo para o Brasil"""
    result = api_requests.get_atendimentos_odontologicos(None, None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert result['2023'] = 0
    assert result['2023'] = 0


def test_get_gravidas_brasil():
    """Testa a função get_gravidas para o Brasil"""
    result = api_requests.get_collection(
        None, None, None, "Gravidez", "6 ou mais atendimentos"
    )
    assert result is not None, "Erro ao fazer a requisição"
    assert result['2023'] = 0
    assert result['2023'] = 0


def test_get_codigos_brasil():
    """Testa a função get_codigos para o Brasil"""
    result = api_requests.get_codigos(None, None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert result['2023'] = 0
    assert result['2023'] = 0