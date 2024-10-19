"""Módulo com os callbacks da página Principal"""
import json

import dash
import dash.dependencies as dd
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import requests
from dash import ALL, Input, Output, State

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

file_path = "data/atendimentos.json"

with open(file_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)


def get_df_atendimentos(json_data):
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

    # TODO normalizar valores pelo total da população (1000 habitantes)

    return df


def get_df_altas(json_data):
    # Para transformar um json de atendimento em um df que será utilizado para gerar os gráficos
    #    json_data -> json que contem os dados de atendimento
    # retorna o df
    dados = []

    # Iterar sobre os anos (2013, 2014, etc.)
    for ano, meses in json_data.items():
        # Iterar sobre os meses e seus valores
        for mes, valor in meses.items():
            # Adicionar uma linha para cada entrada
            dados.append([int(ano), trimestre_map[mes], mes_map[mes], valor])

    # Criar o DataFrame com as colunas: tipo, ano, mês, valor
    df = pd.DataFrame(dados, columns=["ano", "trimestre", "mes", "valor"])
    # df['trimestre'] = df['mes'].apply(calcular_trimestre)
    df["ano_mes"] = df["mes"].astype(str) + "/" + df["ano"].astype(str)
    df["ano_trimestre"] = (
        df["trimestre"].astype(str) + "/" + df["ano"].astype(str)
    )

    # TODO normalizar valores pelo total da população (1000 habitantes)

    return df


def get_df_encaminhamentos(json_data):
    # Para transformar um json de atendimento em um df que será utilizado para gerar os gráficos
    #    json_data -> json que contem os dados de atendimento
    # retorna o df
    dados = []

    # Iterar sobre os anos (2013, 2014, etc.)
    for ano, meses in json_data.items():
        # Iterar sobre os meses e seus valores
        for mes, valor in meses.items():
            # Adicionar uma linha para cada entrada
            dados.append([int(ano), trimestre_map[mes], mes_map[mes], valor])

    # Criar o DataFrame com as colunas: tipo, ano, mês, valor
    df = pd.DataFrame(dados, columns=["ano", "trimestre", "mes", "valor"])
    # df['trimestre'] = df['mes'].apply(calcular_trimestre)
    df["ano_mes"] = df["mes"].astype(str) + "/" + df["ano"].astype(str)
    df["ano_trimestre"] = (
        df["trimestre"].astype(str) + "/" + df["ano"].astype(str)
    )

    # TODO normalizar valores pelo total da população (1000 habitantes)

    return df


def get_big_numbers_atendimentos(df, ano):
    # Para obter os big numbers que devem aparecer como resumo
    #    df -> dados para gerar o gráfico que deve conter ['tipo', 'ano']
    #    ano -> int, ano que foi selecionado para trazer os dados
    # retorna lista com o total do ano e abertura por médico, enfermeiro e outros
    total_ano = df[df["ano"] == ano]["valor"].sum()
    medico = df[(df["profissional"] == "medico") & (df["ano"] == ano)][
        "valor"
    ].sum()
    enfermeiro = df[(df["profissional"] == "enfermeiro") & (df["ano"] == ano)][
        "valor"
    ].sum()
    outros = df[(df["profissional"] == "outros") & (df["ano"] == ano)][
        "valor"
    ].sum()

    return [total_ano, medico, enfermeiro, outros]


type_color_map = {
    "brasil": ["#B36CA3", "#632956", "#3B032F"],
    "estado": ["#80B0DC", "#34679A", "#11173F"],
    "regiao_saude": ["#97C471", "#2B7B6F", "#11302B"],
    "municipio": ["#FFC20D", "#F7941C", "#A7620E"],
}


def update_layout_chart(chart, title, type):
    # Para atualizar o layout do gráfico
    #    chart -> o gráfico que vamos alterar
    #    title -> string com o nome que deve aparecer no label do gráfico
    #    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    # retorna o gráfico atualizado

    color = type_color_map.get(type, [None])[1]

    chart.update_traces(
        textposition="outside",
        marker_color=color,
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#343A40", font_size=12),
        hovertemplate=f"<b>%{{y:,.0f}}</b><br>{title} em %{{x}}<extra></extra>",
    )

    chart.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="#FFFFFF",
        yaxis=dict(showticklabels=False),
        margin=dict(l=35, r=35, t=60, b=40),
    )

    return chart


def update_layout_chart_profissionais(chart, title, type):
    # Para atualizar o layout do gráfico
    #    chart -> o gráfico que vamos alterar
    #    title -> string com o nome que deve aparecer no label do gráfico
    #    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    # retorna o gráfico atualizado

    color1 = type_color_map.get(type, [None])[0]
    color2 = type_color_map.get(type, [None])[1]

    # Aplicar as duas cores alternadamente
    chart.update_traces(
        textposition="outside",
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#343A40", font_size=12),
        hovertemplate=f"<b>%{{y:,.0f}}</b><br>{title} por %{{fullData.name}} em %{{x}}<extra></extra>",
    )

    chart.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend_title=None,
        plot_bgcolor="#FFFFFF",
        yaxis=dict(showticklabels=False),
        margin=dict(l=35, r=35, t=60, b=40),
        legend=dict(
            orientation="h", yanchor="bottom", y=1
        ),  # , xanchor="center", x=0.5 )
    )

    return chart


def get_chart_by_year_profissionais(df, title, type):
    # Retorna o gráfico de barras com o total acumulado dos últimos 6 anos de dados
    #    df -> dados para gerar o gráfico que deve conter ['ano', 'valor']
    #    title -> string com o nome que deve aparecer no label do gráfico
    #    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    # retorna o gráfico gerado

    # Agrupar os dados por ano e quarter somando os valores
    df = df[
        (df["profissional"] == "medico") | (df["profissional"] == "enfermeiro")
    ]
    df_grouped = (
        df.groupby(["profissional", "ano"], observed=True)["valor"]
        .sum()
        .reset_index()
    )
    df_grouped = df_grouped.sort_values("ano")
    df_filtered = df_grouped.tail(6 * df_grouped["profissional"].nunique())

    color1 = type_color_map.get(type, [None])[0]
    color2 = type_color_map.get(type, [None])[1]

    # Criar gráfico de barras empilhadas
    chart = px.bar(
        df_filtered,
        x="ano",
        y="valor",
        color="profissional",  # Agrupar por profissional
        text_auto=".2s",
        title=f"{title.capitalize()} por Ano",
        labels={
            "ano": "Ano",
            "valor": "Valor",
            "profissional": "Profissional",
        },
        color_discrete_map={  # Mapear cores específicas para cada profissional
            "medico": color1,
            "enfermeiro": color2,
        },
    )

    # Atualizar para o layout padrão
    chart = update_layout_chart_profissionais(chart, title, type)

    return chart


def get_chart_by_year(df, title, type):
    # Retorna o gráfico de barras com o total acumulado dos últimos 6 anos de dados
    #    df -> dados para gerar o gráfico que deve conter ['ano', 'valor']
    #    title -> string com o nome que deve aparecer no label do gráfico
    #    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    # retorna o gráfico gerado

    # Agrupar os dados por ano e quarter somando os valores
    df_grouped = (
        df.groupby(["ano"], observed=True)["valor"].sum().reset_index()
    )
    df_grouped = df_grouped.sort_values("ano")
    df_filtered = df_grouped.tail(6)

    # Criar gráfico de barras
    chart = px.bar(
        df_filtered,
        x="ano",
        y="valor",
        text_auto=".2s",
        title=f"{title.capitalize()} por Ano",
    )

    # Atualizar para o layout padrão
    chart = update_layout_chart(chart, title, type)

    return chart


def get_chart_by_quarter(df, title, type):
    # Retorna o gráfico de barras com o total acumulado dos últimos 6 trimestres de dados
    #    df -> dados para gerar o gráfico que deve conter ['ano_trimestre', 'ano', 'trimestre', 'valor']
    #    title -> string com o nome que deve aparecer no label do gráfico
    #    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    # retorna o gráfico gerado

    # Agrupar os dados por ano e quarter somando os valores
    df_grouped = (
        df.groupby(["ano_trimestre", "ano", "trimestre"], observed=True)[
            "valor"
        ]
        .sum()
        .reset_index()
    )
    df_grouped["ano_order"] = df_grouped["ano"].astype(str) + df_grouped[
        "trimestre"
    ].astype(str).str.replace("T", "")
    df_grouped = df_grouped.sort_values("ano_order")
    df_filtered = df_grouped.tail(6)

    # Criar gráfico de barras
    chart = px.bar(
        df_filtered,
        x="ano_trimestre",
        y="valor",
        text_auto=".2s",
        title=f"{title.capitalize()} por Trimestre",
    )

    # Atualizar para o layout padrão
    chart = update_layout_chart(chart, title, type)

    return chart


def get_cities(estado):
    url = f"https://dash-saude-mongo.elsvital.dev/api/v1/cities/{estado}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        cities = response.json()
        return cities
    else:
        print(response.status_code)
        print(response.text)
        return None


def get_ibge_code(estado, municipio):
    """Função para obter o código IBGE de um município a partir do nome e do estado"""
    with open("data/municipios.json", "r", encoding="utf-8") as file:
        municipios = json.load(file)

    for item in municipios:
        if item["estado"] == estado and item["municipio"] == municipio:
            return item["ibge"]

    return None


def get_atendimentos(estado, cidade):
    """Função para obter os dados de atendimentos"""
    url = "https://dash-saude-mongo.elsvital.dev/api/v1/atendimentos"
    if estado is not None:
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/atendimentos/states/{estado}"
    if cidade is not None:
        ibge_code = get_ibge_code(estado, cidade)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/atendimentos/cities/{ibge_code}"

    print("Fazendo request para:", url)

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.text)
        return None


def get_altas(estado, cidade):
    """Função para obter os dados de altas"""
    url = "https://dash-saude-mongo.elsvital.dev/api/v1/altas"
    if estado is not None:
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/altas/states/{estado}"
    if cidade is not None:
        ibge_code = get_ibge_code(estado, cidade)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/altas/cities/{ibge_code}"
    print("Fazendo request para:", url)
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.text)
        return None


def get_encaminhamentos(estado, cidade):
    """Função para obter os dados de encaminhamentos"""
    url = "https://dash-saude-mongo.elsvital.dev/api/v1/encaminhamentos"
    if estado is not None:
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/encaminhamentos/states/{estado}"
    if cidade is not None:
        ibge_code = get_ibge_code(estado, cidade)
        url = f"https://dash-saude-mongo.elsvital.dev/api/v1/encaminhamentos/cities/{ibge_code}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.text)
        return None


df_atendimentos = get_df_atendimentos(json_data)
# df_altas = get_df_altas(json_data)
anos = [2024, 2023, 2022, 2021, 2020, 2019]


def register_callbacks(app):
    @app.callback(
        dd.Output("dropdown-cidade", "options"),
        dd.Input("dropdown-estado", "value"),
    )
    def update_dropdown_cidades(estado):
        # Função para atualizar as opções do dropdown de cidades
        if estado is None:
            raise dash.exceptions.PreventUpdate

        # Filtrar as cidades do estado selecionado
        cidades = get_cities(estado)

        # Transformar em um formato aceito pelo dropdown
        options = [{"label": cidade, "value": cidade} for cidade in cidades]

        return options

    # Callback para fazer a requisição à API e armazenar os dados no dcc.Store
    @app.callback(
        [
            dd.Output("store-data", "data"),
            dd.Output("store-data-altas", "data"),
            dd.Output("store-data-enc", "data"),
        ],
        [
            dd.Input("dropdown-cidade", "value"),
            dd.Input("dropdown-estado", "value"),
        ],
    )
    def fetch_data(cidade, estado):
        """Função para fazer a requisição à API e armazenar os dados no dcc.Store"""
        data_atendimentos = get_atendimentos(estado, cidade)
        data_altas = get_altas(estado, cidade)
        data_encaminhamentos = get_encaminhamentos(estado, cidade)

        return data_atendimentos, data_altas, data_encaminhamentos

    @app.callback(
        [
            Output("total-atendimentos", "children"),
            Output("big-medicos", "children"),
            Output("big-enfermeiros", "children"),
            Output("big-outros", "children"),
        ],
        [
            Input("store-data", "data"),
            *[Input(f"btn-{ano}", "n_clicks") for ano in anos],
        ],
        [
            State("store-data", "data"),
            *[State(f"btn-{ano}", "n_clicks") for ano in anos],
        ],
    )
    def update_big_numbers(data, *args):
        ctx = dash.callback_context

        # Identificar o ano selecionado
        ano = anos[0]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-ano" in prop_id:
                ano = int(
                    ctx.triggered[0]["prop_id"].split(".")[0].split("-")[-1]
                )  # Extrai o ano do ID do botão

        df = get_df_atendimentos(data)
        big_numbers = get_big_numbers_atendimentos(df, ano)

        # Dividir cada big number por 1000 para facilitar a leitura
        big_numbers = [int(num / 1000) for num in big_numbers]

        return big_numbers

    # Callback para atualiza os totais de altas
    @app.callback(
        [
            Output("total-altas", "children"),
            Output("total-encaminhamentos", "children"),
        ],
        [
            Input("store-data-altas", "data"),
            Input("store-data-enc", "data"),
        ],
    )
    def update_totals(data_altas, data_encaminhamentos):
        df_altas = get_df_altas(data_altas)
        df_encaminhamentos = get_df_encaminhamentos(data_encaminhamentos)

        total_altas = int(df_altas["valor"].sum() / 1000)
        total_encaminhamentos = int(df_encaminhamentos["valor"].sum() / 1000)

        return total_altas, total_encaminhamentos

    # Callback para atualizar os gráficos de atendimentos com base nos dados armazenados
    @app.callback(
        [
            Output("chart_by_year", "figure"),
            Output("chart_by_year_profissionais", "figure"),
            Output("chart_by_quarter", "figure"),
        ],
        Input("store-data", "data"),
    )
    def update_charts(data):
        df_atendimentos = get_df_atendimentos(data)

        # Gerar os gráficos
        chart_by_year = get_chart_by_year(
            df_atendimentos, "atendimentos", "brasil"
        )
        chart_by_year_profissionais = get_chart_by_year_profissionais(
            df_atendimentos, "atendimentos", "brasil"
        )
        chart_by_quarter = get_chart_by_quarter(
            df_atendimentos, "atendimentos", "brasil"
        )

        return chart_by_year, chart_by_year_profissionais, chart_by_quarter

    @app.callback(
        Output("chart_altas", "figure"), Input("store-data-altas", "data")
    )
    def update_chart_altas(data):
        df_altas = get_df_altas(data)

        # Gerar o gráfico
        chart_altas = get_chart_by_year(df_altas, "altas", "brasil")

        return chart_altas

    @app.callback(
        Output("chart_encaminhamentos", "figure"),
        Input("store-data-enc", "data"),
    )
    def update_chart_encaminhamentos(data):
        df_encaminhamentos = get_df_encaminhamentos(data)

        # Gerar o gráfico
        chart_encaminhamentos = get_chart_by_year(
            df_encaminhamentos, "encaminhamentos", "brasil"
        )

        return chart_encaminhamentos
