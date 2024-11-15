"""Módulo de testes para o arquivo producao_profissionais_individual.csv"""

import pandas as pd
import pytest

FILE_NAME = "producao_profissionais_individual.csv"
ANO = 2023

# Carregar o arquivo
df = pd.read_csv(f"../etl/data/consolidado/{FILE_NAME}")


def test_sum_enfermeiro_for_sp():
    """Testa a soma de enfermeiros em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Enfermeiro"].sum()
    expected_value = 19927236
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_medico_for_sp():
    """Testa a soma de médicos em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Médico"].sum()
    expected_value = 50039489
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_agente_comunitario_de_saude_for_sp():
    """Testa a soma de agentes comunitários de saúde em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)][
        "Agente comunitário de saúde"
    ].sum()
    expected_value = 0
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_assistente_social_for_sp():
    """Testa a soma de assistentes sociais em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)][
        "Assistente Social"
    ].sum()
    expected_value = 732032
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_fonoaudiologo_for_sp():
    """Testa a soma de fonoaudiólogos em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Fonoaudiólogo"].sum()
    expected_value = 415121
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_fisioterapeutico_for_sp():
    """Testa a soma de fisioterapeutas em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)][
        "Fisioterapeuta"
    ].sum()
    expected_value = 1166401
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_enfermeiro_for_araras():
    """Testa a soma de enfermeiros em Araras"""
    result = df[(df["Municipio"] == "ARARAS") & (df["Ano"] == ANO)][
        "Enfermeiro"
    ].sum()
    expected_value = 27305
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_medico_for_araras():
    """Testa a soma de médicos em Araras"""
    result = df[(df["Municipio"] == "ARARAS") & (df["Ano"] == ANO)][
        "Médico"
    ].sum()
    expected_value = 83052
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_agente_comunitario_de_saude_for_araras():
    """Testa a soma de agentes comunitários de saúde em Araras"""
    result = df[(df["Municipio"] == "ARARAS") & (df["Ano"] == ANO)][
        "Agente comunitário de saúde"
    ].sum()
    expected_value = 0
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_nutricionista_for_araras():
    """Testa a soma de nutricionistas em Araras"""
    result = df[(df["Municipio"] == "ARARAS") & (df["Ano"] == ANO)][
        "Nutricionista"
    ].sum()
    expected_value = 41
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


if __name__ == "__main__":
    # Executa os testes e imprime os resultados
    pytest.main([__file__])
