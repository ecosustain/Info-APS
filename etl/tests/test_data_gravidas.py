"""Módulo de testes para o arquivo gravidas.csv"""

import pandas as pd
import pytest

FILE_NAME = "gravidas.csv"
ANO = 2023
MES = "JAN"

# Carregar o arquivo
df = pd.read_csv(f"../etl/data/consolidado/{FILE_NAME}")


def test_sum_gravidas_for_sp():
    """Testa a soma de grávidas em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO) & (df["Mes"] == MES)][
        "De 1 a 3 atendimentos"
    ].sum()
    expected_value = 15943
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


def test_sum_gravidas_for_br():
    """Testa a soma de grávidas no Brasil"""
    result = df[(df["Ano"] == ANO) & (df["Mes"] == MES)][
        "De 1 a 3 atendimentos"
    ].sum()
    expected_value = 92360
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


def test_sum_gravidas_for_araras():
    """Testa a soma de grávidas em Araras"""
    result = df[
        (df["Municipio"] == "ARARAS") & (df["Ano"] == ANO) & (df["Mes"] == MES)
    ]["De 1 a 3 atendimentos"].sum()
    expected_value = 23
    assert result == expected_value, f"Esperado {expected_value}, mas obteve {result}"


if __name__ == "__main__":
    # Executa os testes e imprime os resultados
    pytest.main([__file__])
