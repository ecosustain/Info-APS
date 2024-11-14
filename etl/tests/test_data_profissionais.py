"""Módulo de testes para o arquivo producao_profissionais_individual.csv"""

import pandas as pd
import pytest

FILE_NAME = "producao_profissionais_individual.csv"
ANO = 2024

# Carregar o arquivo
df = pd.read_csv(f"../etl/data/consolidado/{FILE_NAME}")


def test_sum_enfermeiro_for_sp():
    """Testa a soma de enfermeiros em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Enfermeiro"].sum()
    expected_value = 16309713
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


def test_sum_medico_for_sp():
    """Testa a soma de médicos em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Médico"].sum()
    expected_value = 40945197
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


def test_sum_agente_comunitario_de_saude_for_sp():
    """Testa a soma de agentes comunitários de saúde em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)][
        "Agente comunitário de saúde"
    ].sum()
    expected_value = 0
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


def test_sum_assistente_social_for_sp():
    """Testa a soma de assistentes sociais em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Assistente Social"].sum()
    expected_value = 568523
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


def test_sum_fonoaudiologo_for_sp():
    """Testa a soma de fonoaudiólogos em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Fonoaudiólogo"].sum()
    expected_value = 325169
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


def test_sum_fisioterapeutico_for_sp():
    """Testa a soma de fisioterapeutas em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Fisioterapeuta"].sum()
    expected_value = 964614
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


if __name__ == "__main__":
    # Executa os testes e imprime os resultados
    pytest.main([__file__])
