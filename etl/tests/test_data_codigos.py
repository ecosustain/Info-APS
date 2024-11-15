"""Módulo de testes para o arquivo producao_codigos.csv"""

import pandas as pd
import pytest

FILE_NAME = "producao_codigos.csv"
ANO = 2023

# Carregar o arquivo
df = pd.read_csv(f"../etl/data/consolidado/{FILE_NAME}")


def test_sum_febre_sp():
    """Testa a soma de atendimentos por febre em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)][
        "CIAP (A03) Febre"
    ].sum()
    expected_value = 82625
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_febre_br():
    """Testa a soma de atendimentos por febre no Brasil"""
    result = df[(df["Ano"] == ANO)]["CIAP (A03) Febre"].sum()
    expected_value = 956655
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_febre_araras():
    """Testa a soma de atendimentos por febre em Araras"""
    result = df[(df["Municipio"] == "ARARAS") & (df["Ano"] == ANO)][
        "CIAP (A03) Febre"
    ].sum()
    expected_value = 92
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


if __name__ == "__main__":
    # Executa os testes e imprime os resultados
    pytest.main([__file__])
