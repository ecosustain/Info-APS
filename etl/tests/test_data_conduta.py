"""Módulo para testar os dados de encaminhamentos"""

import pandas as pd
import pytest

ANO = 2023

# Carregar o arquivo
df = pd.read_csv("../etl/data/consolidado/producao_conduta.csv")


def test_sum_encaminhamentos_for_sp():
    """Testa a soma de encaminhamentos em SP"""
    result = df[(df["Uf"] == "SP") & (df["Ano"] == ANO)][
        "Retorno para consulta agendada"
    ].sum()
    expected_value = 20641920
    assert (
        result == expected_value
    ), f"Esperado {expected_value}, mas obteve {result}"


if __name__ == "__main__":
    # Executa os testes e imprime os resultados
    pytest.main([__file__])
