"""Módulo para processar os dados obtidos da API e transformá-los para gerar os gráficos"""

import dash
import pandas as pd

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


def get_df_atendimentos(json_data, populacao=None):
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
        populacao = populacao / 1000
        df["valor"] = df["valor"] / populacao
        df["valor"] = df["valor"].astype(int)

    return df


def get_df_from_json(json_data, populacao=None):
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
    df = pd.DataFrame(
        dados, columns=["ano", "trimestre", "mes", "valor"]
    )
    # df['trimestre'] = df['mes'].apply(calcular_trimestre)
    df["ano_mes"] = df["mes"].astype(str) + "/" + df["ano"].astype(str)
    df["ano_trimestre"] = (
        df["trimestre"].astype(str) + "/" + df["ano"].astype(str)
    )

    # normalizar valores pelo total da população (1000 habitantes)
    if populacao is not None:
        populacao = populacao / 1000
        df["valor"] = df["valor"] / populacao
        df["valor"] = df["valor"].astype(int)

    return df

def get_df_encaminhamentos(json_data, json_atendimentos, populacao=None):
    """Função para transformar um json de encaminhamentos em um df que será utilizado para gerar os gráficos"""
    # Para transformar um json de atendimento em um df que será utilizado para gerar os gráficos
    #    json_data -> json que contem os dados de encaminhamento
    #    json_atendimentos -> json que contem os dados de atendimento
    #    populacao -> valor da população caso exista 
    # retorna o df
    df = get_df_from_json(json_data)

    if json_atendimentos is not None:
        atendimento = get_df_atendimentos(json_atendimentos)
        df = pd.merge(df, atendimento, on=["ano", "trimestre", "mes", "ano_mes"], suffixes=('_1', '_2'))
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
    enfermeiro = df[(df["profissional"] == "enfermeiro") & (df["ano"] == ano)][
        "valor"
    ].sum()
    return [total_ano, medico, enfermeiro]
