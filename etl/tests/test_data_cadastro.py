"""Módulo de testes para o arquivo Cadastro.csv"""

import pandas as pd
import pytest

FILE_NAME = "Cadastro.csv"
ANO = 2023

# Carregar o arquivo
df = pd.read_csv(f"../etl/data/consolidado/{FILE_NAME}")


def test_sum_for_sp():
    """Testa a soma de cadastros em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)]["Cadastros"].sum()
    expected_value = 379197375
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_for_rj():
    """Testa a soma de cadastros no RJ"""
    result = df[(df["Uf"] == "RJ") & (df["Ano"] == ANO)]["Cadastros"].sum()
    expected_value = 144685747
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_for_br():
    """Testa a soma de cadastros no Brasil"""
    result = df[df["Ano"] == ANO]["Cadastros"].sum()
    expected_value = 2111681269
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


def test_sum_for_araras():
    """Testa a soma de cadastros em Araras"""
    result = df[(df["Municipio"] == "ARARAS") & (df["Ano"] == ANO)][
        "Cadastros"
    ].sum()
    expected_value = 1170198
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


if __name__ == "__main__":
    # Executa os testes e imprime os resultados
    pytest.main([__file__])
