"""Módulo para testar as requisicoes da API"""

import pytest

from painel.api import api_requests

ANO = "2023"


def test_get_atendimentos_brasil():
    """Testa a função get_atendimentos para o Brasil"""
    result = api_requests.get_atendimentos(None, None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert sum(result["enfermeiro"][ANO].values()) == 116782858
    assert sum(result["medico"][ANO].values()) == 216879591
    assert (
        sum(
            sum(anos["2023"].values())
            for profissional, anos in result.items()
            if "2023" in anos
        )
        == 356894032
    )


def test_get_atendimentos_sp():
    """Testa a função get_atendimentos para SP"""
    result = api_requests.get_atendimentos("SP", None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert sum(result["enfermeiro"][ANO].values()) == 19927236
    assert sum(result["medico"][ANO].values()) == 50039489
    assert (
        sum(
            sum(anos["2023"].values())
            for profissional, anos in result.items()
            if "2023" in anos
        )
        == 74981068
    )


def test_get_atendimentos_adamantina():
    """Testa a função get_atendimentos para Adamantina"""
    result = api_requests.get_atendimentos("SP", "ADAMANTINA", None)
    assert result is not None, "Erro ao fazer a requisição"
    assert sum(result["enfermeiro"][ANO].values()) == 112002
    assert sum(result["medico"][ANO].values()) == 242979


def test_get_atendimentos_araras():
    """Testa a função get_atendimentos para Araras"""
    result = api_requests.get_atendimentos("SP", None, "ARARAS")
    assert result is not None, "Erro ao fazer a requisição"
    assert sum(result["enfermeiro"][ANO].values()) == 27305
    assert sum(result["medico"][ANO].values()) == 83052


def test_get_visitas_sp():
    """Testa a função get_visitas_domiciliar para o estado de SP"""
    result = api_requests.get_visitas_domiciliar("SP", None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert sum(result[ANO].values()) == 70556064


def test_get_odonto_sp():
    """Testa a função get_odontologo para o estado de SP"""
    result = api_requests.get_atendimentos_odontologicos("SP", None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert sum(result[ANO].values()) == 9228913


def test_get_gravidas_brasil():
    """Testa a função get_gravidas para o Brasil"""
    result = api_requests.get_collection(
        None, None, None, "Gravidez", "6 ou mais atendimentos"
    )
    assert result is not None, "Erro ao fazer a requisição"
    assert result[ANO]["JAN"] == 66909


def test_get_encaminhamentos_sp():
    """Testa a função get_encaminhamentos para SP"""
    result = api_requests.get_encaminhamentos("SP", None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert sum(result[ANO].values()) == 6335699


"""
def test_get_codigos_brasil():
    """  # Testa a função get_codigos para o Brasil"""
"""
    result = api_requests.get_codigos(None, None, None)
    assert result is not None, "Erro ao fazer a requisição"
    assert result['2023'] == 0
    assert result['2023'] == 0
    """


if __name__ == "__main__":
    # Executa os testes e imprime os resultados
    pytest.main([__file__])
