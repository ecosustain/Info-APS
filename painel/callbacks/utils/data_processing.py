"""Módulo para processar os dados obtidos da API e transformá-los para gerar os gráficos"""

from collections import defaultdict
from typing import Dict

import pandas as pd
from api.api_requests import (
    get_atendimentos_individuais_problema,
    get_collection,
    get_collection_atributes,
)

# Mapeamento dos meses para seus números correspondentes
mes_map = {
    "JAN": 1,
    "FEV": 2,
    "MAR": 3,
    "ABR": 4,
    "MAI": 5,
    "JUN": 6,
    "JUL": 7,
    "AGO": 8,
    "SET": 9,
    "OUT": 10,
    "NOV": 11,
    "DEZ": 12,
}
# Mapeamento dos meses para seus trimestres correspondentes
trimestre_map = {
    "JAN": "T1",
    "FEV": "T1",
    "MAR": "T1",
    "ABR": "T2",
    "MAI": "T2",
    "JUN": "T2",
    "JUL": "T3",
    "AGO": "T3",
    "SET": "T3",
    "OUT": "T4",
    "NOV": "T4",
    "DEZ": "T4",
}

trimestre_map_num = {
    1: "T1",
    2: "T1",
    3: "T1",
    4: "T2",
    5: "T2",
    6: "T2",
    7: "T3",
    8: "T3",
    9: "T3",
    10: "T4",
    11: "T4",
    12: "T4",
}


def get_df_atendimentos(json_data, populacao=None, qtd_hab=1000):
    """Função para transformar um json de atendimento em um df que será utilizado para gerar os gráficos"""
    # Para transformar um json de atendimento em um df que será utilizado para gerar os gráficos
    #    json_data -> json que contem os dados de atendimento
    # retorna o df
    dados = []

    # Iterar sobre os diferentes tipos (enfermeiro, médico, etc.)
    for profissional, anos in json_data.items():
        # Iterar sobre os anos (2013, 2014, etc.)
        for ano, meses in anos.items():
            # Iterar sobre os meses e seus valores
            for mes, valor in meses.items():
                # Adicionar uma linha para cada entrada
                dados.append(
                    [
                        profissional,
                        int(ano),
                        trimestre_map[mes],
                        mes_map[mes],
                        valor,
                    ]
                )
    # Criar o DataFrame com as colunas: profissional, ano, mês, valor
    df = pd.DataFrame(
        dados, columns=["profissional", "ano", "trimestre", "mes", "valor"]
    )
    # df['trimestre'] = df['mes'].apply(calcular_trimestre)
    df["ano_mes"] = df["mes"].astype(str) + "/" + df["ano"].astype(str)
    df["ano_trimestre"] = (
        df["trimestre"].astype(str) + "/" + df["ano"].astype(str)
    )

    # normalizar valores pelo total da população (1000 habitantes)
    if populacao is not None:
        # filtrar df pelos ultimos 6 anos
        df_filtrado = df[df["ano"] >= (df["ano"].max() - 6)]
        # normalizar valor pela populacao pra cada ano
        df_filtrado["valor"] = df_filtrado.apply(
            lambda row: row["valor"] / (populacao[str(row["ano"])] / qtd_hab),
            axis=1,
        )
        df = df_filtrado

    return df


def get_df_from_json(json_data, populacao=None, qtd_hab=1000):
    """Função para transformar um json (ex: visitas, atendimentos odontologicos) em um df que será utilizado para gerar os gráficos"""
    # Para transformar um json de atendimento em um df que será utilizado para gerar os gráficos
    #    json_data -> json que contem os dados de atendimento
    #    populacao -> valor da população caso exista
    # retorna o df
    dados = []

    # Iterar sobre os anos (2013, 2014, etc.)
    for ano, meses in json_data.items():
        # Iterar sobre os meses e seus valores
        for mes, valor in meses.items():
            # Adicionar uma linha para cada entrada
            dados.append(
                [
                    int(ano),
                    trimestre_map[mes],
                    mes_map[mes],
                    valor,
                ]
            )
    # Criar o DataFrame com as colunas: profissional, ano, mês, valor
    df = pd.DataFrame(dados, columns=["ano", "trimestre", "mes", "valor"])
    # df['trimestre'] = df['mes'].apply(calcular_trimestre)
    df["ano_mes"] = df["mes"].astype(str) + "/" + df["ano"].astype(str)
    df["ano_trimestre"] = (
        df["trimestre"].astype(str) + "/" + df["ano"].astype(str)
    )

    # normalizar valores pelo total da população (1000 habitantes)
    if populacao is not None:
        # filtrar df pelos ultimos 6 anos
        df_filtrado = df[df["ano"] >= (df["ano"].max() - 6)]
        # normalizar valor pela populacao pra cada ano
        df_filtrado["valor"] = df_filtrado.apply(
            lambda row: row["valor"] / (populacao[str(row["ano"])] / qtd_hab),
            axis=1,
        )
        df = df_filtrado

    return df


def get_df_encaminhamentos(
    json_data, json_atendimentos, populacao=None, total=False
):
    """Função para transformar um json de encaminhamentos em um df que será utilizado para gerar os gráficos"""
    # Para transformar um json de atendimento em um df que será utilizado para gerar os gráficos
    #    json_data -> json que contem os dados de encaminhamento
    #    json_atendimentos -> json que contem os dados de atendimento
    #    populacao -> valor da população caso exista
    # retorna o df
    df = get_df_from_json(json_data)

    if json_atendimentos is not None:
        if total:
            atendimento = get_df_from_json(json_atendimentos)
        else:
            atendimento = get_df_atendimentos(json_atendimentos)
        df = pd.merge(
            df,
            atendimento,
            on=["ano", "ano_trimestre", "trimestre", "mes", "ano_mes"],
            suffixes=("_1", "_2"),
        )
        df["valor"] = df["valor_1"]

    # normalizar valores pelo total da população (1000 habitantes)
    if populacao is not None:
        populacao = populacao / 1000
        df["valor"] = df["valor"] / populacao
        df["valor"] = df["valor"].astype(int)

    return df


def get_big_numbers_atendimentos(df, ano):
    """Para obter os big numbers que devem aparecer como resumo
    #    df -> dados para gerar o gráfico que deve conter ['tipo', 'ano']
    #    ano -> int, ano que foi selecionado para trazer os dados
    # retorna lista com o total do ano e abertura por médico, enfermeiro e outros
    """
    total_ano = df[df["ano"] == ano]["valor"].sum()
    medico = df[(df["profissional"] == "medico") & (df["ano"] == ano)][
        "valor"
    ].sum()

    return [total_ano, medico]


def get_gravidez_json(estado, regiao, municipio):
    """Função para obter o indice de gravidez"""
    adequado = get_collection(
        estado, regiao, municipio, "Gravidez", "6 ou mais atendimentos"
    )
    inadequado = get_collection(
        estado,
        regiao,
        municipio,
        "Gravidez",
        "De 1 a 3 atendimentos,De 4 a 5 atendimentos",
    )
    return adequado, inadequado


def get_df_gravidez(json_adequado, json_inadequado):
    """Função para transformar um json de gravidez adequado e inadequado em um df que será utilizado para gerar os gráficos"""
    # Para transformar um json de atendimento em um df que será utilizado para gerar os gráficos
    #    json_adequado -> json que contem os dados de gravidez adequado
    #    json_inadequado -> json que contem os dados de gravidez inadequado
    # retorna o df
    df_adequado = get_df_from_json(json_adequado)
    df_inadequado = get_df_from_json(json_inadequado)

    df = pd.merge(
        df_adequado,
        df_inadequado,
        on=["ano", "ano_trimestre", "trimestre", "mes", "ano_mes"],
        suffixes=("_1", "_inadequado"),
    )

    df["valor_2"] = df["valor_1"] + df["valor_inadequado"]
    df["valor"] = df["valor_1"]

    return df


def get_atributos_febre():
    """Função para obter os atributos de febre"""
    atributos = get_collection_atributes("CIDS")
    remover = ["CIAP (N01) Cefaléia", "CIAP (R05) Tosse"]
    for r in remover:
        atributos.remove(r)
    # Concatenar os atributos, separando-os por vírgula
    atributos = ",".join(atributos)
    return atributos


def get_cids_json_cefaleia(estado, regiao, municipio):
    """Função para obter os jsons de cids Cefaléia"""
    dor_cabeca = get_collection(
        estado, regiao, municipio, "CIDS", "CIAP (N01) Cefaléia"
    )

    return dor_cabeca

def get_cids_json_tosse(estado, regiao, municipio):
    """Função para obter os jsons de cids Tosse"""
    tosse = get_collection(
        estado, regiao, municipio, "CIDS", "CIAP (R05) Tosse"
    )

    return tosse

def get_cids_json_febre(estado, regiao, municipio):
    """Função para obter os jsons de cids Febre"""
    palavra_febre = get_collection(
        estado, regiao, municipio, "CIDS", "CIAP (A03) Febre"
    )

    return palavra_febre


def get_asma_dpoc_json(estado, regiao, municipio):
    """Função para obter os jsons de asma e dpoc"""
    asma = get_atendimentos_individuais_problema(
        estado, regiao, municipio, "Asma"
    )
    dpoc = get_atendimentos_individuais_problema(
        estado, regiao, municipio, "DPOC"
    )
    # Somar os valores de asma e dpoc
    for ano in asma:
        for mes in asma[ano]:
            if mes in dpoc[ano]:
                asma[ano][mes] += dpoc[ano][mes]
    return asma


def soma_atendimentos(
    atendimentos: Dict[str, Dict[str, Dict[str, int]]]
) -> Dict[str, Dict[str, int]]:
    """
    Função para somar os atendimentos.

    Args:
        atendimentos (Dict[str, Dict[str, Dict[str, int]]]): Dicionário contendo os atendimentos.

    Returns:
        Dict[str, Dict[str, int]]: Dicionário com os totais de atendimentos por ano e mês.
    """
    # Inicializar um defaultdict para armazenar os totais
    total_atendimentos = defaultdict(lambda: defaultdict(int))

    # Iterar sobre os anos e meses para somar os valores
    for anos in atendimentos.values():
        for ano, meses in anos.items():
            for mes, valor in meses.items():
                total_atendimentos[ano][mes] += valor

    # Converter defaultdict para dict antes de retornar
    return {ano: dict(meses) for ano, meses in total_atendimentos.items()}
