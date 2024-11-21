import os

import pandas as pd
import pytest

path = "../shared_data/"
# Lista de arquivos CSV a serem testados
file_list = [
    f"{path}Cadastro.csv",
    f"{path}gravidas.csv",
    f"{path}producao_codigos.csv",
    f"{path}producao_condicao.csv",
    f"{path}producao_conduta.csv",
    f"{path}producao_profissionais_individual.csv",
    f"{path}producao_tipo.csv",
    f"{path}producao_procedimento.csv",
    f"{path}producao_procedimentos_odontologicos.csv",
    f"{path}producao_aleitamento.csv",
    f"{path}producao_vacinacao.csv",
    f"{path}producao_acoes.csv",
    f"{path}producao_racionalidade.csv",
    f"{path}producao_consulta_odontologica.csv",
    f"{path}producao_vigilancia_bucal.csv",
    f"{path}producao_conduta_odontologica.csv",
    f"{path}producao_visita.csv",
    f"{path}producao_desfecho_visita.csv",
    f"{path}producao_imovel.csv",
    f"{path}producao_profissionais_odontologico.csv",
    f"{path}producao_profissionais_procedimentos.csv",
    f"{path}producao_profissionais_visita.csv",
]


@pytest.mark.parametrize("file_path", file_list)
def test_estado(file_path):
    """Vários testes para o campo Estado"""
    df = pd.read_csv(file_path)
    assert df["Uf"].nunique() == 27, "Número de estados incorreto"
    assert df["Uf"].str.len().max() == 2, "Estado com mais de 2 caracteres"
    assert df["Uf"].str.isupper().all(), "Estado com letras minúsculas"
    assert (
        df["Uf"].str.isalpha().all()
    ), "Estado com caracteres não alfabéticos"


@pytest.mark.parametrize("file_path", file_list)
def test_ibge(file_path):
    """Vários testes para o campo IBGE"""
    # Verifica se o arquivo é o cadastro e pula o teste se for
    df = pd.read_csv(file_path)
    df["Ibge"] = df["Ibge"].astype(str)
    # Pula apenas a verificação de quantidade de IBGE únicos para o arquivo de códigos
    assert (
        df["Ibge"].nunique() > 5500
    ), f"Esperado mais de 5500 IBGE únicos, mas obteve {df['Ibge'].nunique()}"
    assert (
        df["Ibge"].astype(str).str.len().max() == 6
    ), f"IBGE com mais de 6 caracteres, mas obteve {df['Ibge'].astype(str).str.len().max()}"
    assert (
        df["Ibge"].astype(str).str.isnumeric().all()
    ), f"IBGE com caracteres não numéricos, mas obteve {df['Ibge'].astype(str).str.isnumeric().all()}"


@pytest.mark.parametrize("file_path", file_list)
def test_ano(file_path):
    """Vários testes para o campo Ano"""
    df = pd.read_csv(file_path)
    assert df["Ano"].dtype == "int64", "Ano não é inteiro"
    assert df["Ano"].max() <= 2025, "Ano maior que 2025"
    assert df["Ano"].min() >= 2013, "Não tem anos antes de 2018"
    assert df["Ano"].min() <= 2018, "Não tem anos antes de 2018"


@pytest.mark.parametrize("file_path", file_list)
def test_mes(file_path):
    """Vários testes para o campo Mes"""
    df = pd.read_csv(file_path)
    assert df["Mes"].str.len().max() == 3, "Mes com mais de 3 caracteres"
    assert df["Mes"].nunique() == 12, "Número de meses incorreto"
    assert df["Mes"].str.isalpha().all(), "Mes com caracteres não alfabéticos"
    assert df["Mes"].str.isupper().all(), "Mes com letras minusculas"


if __name__ == "__main__":
    # Executa todos os testes
    pytest.main([__file__])
