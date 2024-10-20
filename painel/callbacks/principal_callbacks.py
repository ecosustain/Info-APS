"""Módulo com os callbacks da página Principal"""
import json

import dash
import dash.dependencies as dd
import geopandas as gpd
import pandas as pd
import plotly.express as px
import requests
from dash import ALL, Input, Output, State, dcc

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


def get_df_altas(json_data, populacao=None):
    """Função para transformar um json de altas em um df que será utilizado para gerar os gráficos"""
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

    # normalizar valores pelo total da população (1000 habitantes)
    if populacao is not None:
        populacao = populacao / 1000
        df["valor"] = df["valor"] / populacao
        df["valor"] = df["valor"].astype(int)

    return df


def get_df_encaminhamentos(json_data, populacao=None):
    """Função para transformar um json de encaminhamentos em um df que será utilizado para gerar os gráficos"""
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

    # normalizar valores pelo total da população (1000 habitantes)
    if populacao is not None:
        populacao = populacao / 1000
        df["valor"] = df["valor"] / populacao
        df["valor"] = df["valor"].astype(int)

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
            orientation="h",
            yanchor="bottom",
            y=0.95,
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


def get_population(estado, municipio):
    """Função para obter a população de um município, estado ou do Brasil"""
    with open("data/cadastros.json", "r", encoding="utf-8") as file:
        cadastros = json.load(file)

    if municipio is None and estado is None:
        # soma de todas as populações
        total = 0
        for item in cadastros:
            total += item["Cadastros"]
        return total

    if municipio is None:
        # soma da população do estado
        total = 0
        for item in cadastros:
            if item["Uf"] == estado:
                total += item["Cadastros"]
        return total

    for item in cadastros:
        if item["Uf"] == estado and item["Municipio"] == municipio:
            return item["Cadastros"]

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
            Output("store-data", "data"),
            Output("store-data-altas", "data"),
            Output("store-data-enc", "data"),
            Output("store-populacao", "value"),
        ],
        [
            Input("dropdown-cidade", "value"),
            Input("dropdown-estado", "value"),
        ],
    )
    def fetch_data(cidade, estado):
        """Função para fazer a requisição à API e armazenar os dados no dcc.Store"""
        data_atendimentos = get_atendimentos(estado, cidade)
        data_altas = get_altas(estado, cidade)
        data_encaminhamentos = get_encaminhamentos(estado, cidade)
        populacao = get_population(estado, cidade)

        return data_atendimentos, data_altas, data_encaminhamentos, populacao

    @app.callback(
        [
            Output("total-atendimentos", "children"),
            Output("normalizado-atendimentos", "children"),
            Output("big-medicos", "children"),
            Output("big-enfermeiros", "children"),
            Output("big-outros", "children"),
        ],
        [
            Input("store-data", "data"),
            Input("store-populacao", "value"),
            *[Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
        [
            State("store-data", "data"),
            *[State(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
    )
    def update_big_numbers(data, populacao, *args):
        ctx = dash.callback_context

        # Identificar o ano selecionado
        ano = anos[0]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-ano" in prop_id:
                ano = int(
                    ctx.triggered[0]["prop_id"].split(".")[0].split("-")[-1]
                )  # Extrai o ano do ID do botão

        if data is None:
            raise dash.exceptions.PreventUpdate

        df = get_df_atendimentos(data)
        big_numbers = get_big_numbers_atendimentos(df, ano)
        # Normalizar os valores pelo total da população
        total_populacao = populacao / 1000
        total_atendimentos = big_numbers[0]

        # Dividir cada big number por 1000 para facilitar a leitura
        big_numbers = [int(num / total_populacao) for num in big_numbers]

        # Inserir o total de atendimentos no primeiro lugar
        big_numbers.insert(0, total_atendimentos)

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
            Input("store-populacao", "value"),
        ],
    )
    def update_totals(data_altas, data_encaminhamentos, populacao):
        df_altas = get_df_altas(data_altas)
        df_encaminhamentos = get_df_encaminhamentos(data_encaminhamentos)

        total_altas = df_altas[
            "valor"
        ].sum()  # int(df_altas["valor"].sum() / populacao)
        total_encaminhamentos = df_encaminhamentos[
            "valor"
        ].sum()  # int(df_encaminhamentos["valor"].sum() / populacao)

        return total_altas, total_encaminhamentos

    # Callback para atualizar os gráficos de atendimentos com base nos dados armazenados
    @app.callback(
        [
            Output("chart_by_year", "figure"),
            Output("chart_by_year_profissionais", "figure"),
            Output("chart_by_quarter", "figure"),
        ],
        Input("store-data", "data"),
        Input("store-populacao", "value"),
    )
    def update_charts(data, populacao):
        df_atendimentos = get_df_atendimentos(data, populacao)

        # Gerar os gráficos
        chart_by_year = get_chart_by_year(
            df_atendimentos, "Atendimentos totais", "brasil"
        )
        chart_by_year_profissionais = get_chart_by_year_profissionais(
            df_atendimentos, "Atendimentos por profissionais", "brasil"
        )
        chart_by_quarter = get_chart_by_quarter(
            df_atendimentos, "Atendimentos totais", "brasil"
        )

        return chart_by_year, chart_by_year_profissionais, chart_by_quarter

    @app.callback(
        Output("chart_altas", "figure"),
        [Input("store-data-altas", "data"), Input("store-populacao", "value")],
    )
    def update_chart_altas(data, populacao):
        df_altas = get_df_altas(data, populacao)

        # Gerar o gráfico
        chart_altas = get_chart_by_year(
            df_altas, "Altas totais registradas", "brasil"
        )

        return chart_altas

    @app.callback(
        Output("chart_encaminhamentos", "figure"),
        [
            Input("store-data-enc", "data"),
            Input("store-populacao", "value"),
        ],
    )
    def update_chart_encaminhamentos(data, populacao):
        df_encaminhamentos = get_df_encaminhamentos(data, populacao)

        # Gerar o gráfico
        chart_encaminhamentos = get_chart_by_year(
            df_encaminhamentos, "Encaminhamentos totais registrados", "brasil"
        )

        return chart_encaminhamentos

    @app.callback(
        dd.Output("mapa-estado", "figure"), [Input("mapa-estado", "clickData")]
    )
    def update_map(mapa):
        shapefile_uf = "../mapas/BR_UF_2022/BR_UF_2022.shp"
        brasil_estados = gpd.read_file(shapefile_uf)

        mapa_uf = brasil_estados[["SIGLA_UF", "geometry"]]

        mapa_uf["geometry"] = brasil_estados["geometry"].simplify(
            tolerance=0.01
        )

        mapa_uf["value"] = 1

        fig = px.choropleth(
            mapa_uf,
            geojson=mapa_uf.geometry,  # Usar a geometria do shapefile
            locations=mapa_uf.index,  # Nome da coluna do DataFrame
            hover_name="SIGLA_UF",
            hover_data={"SIGLA_UF": False, "value": False},
            color="value",
            color_continuous_scale=[
                "#B36CA3",
                "#B36CA3",
                "#B36CA3",
            ],
        )

        # Ajustar as configurações do mapa
        fig.update_geos(
            fitbounds="locations",
            visible=False,
        )
        fig.update_layout(
            margin={"r": 0, "t": 50, "l": 0, "b": 0}, coloraxis_showscale=False
        )

        return fig

    # Callback para capturar o clique no estado
    @app.callback(
        Output("dropdown-estado", "value"), [Input("mapa-estado", "clickData")]
    )
    def display_click_data(clickData):
        if clickData is None:
            raise dash.exceptions.PreventUpdate
        state_clicked = clickData["points"][0][
            "location"
        ]  # Extrai a sigla do estado clicado

        estados_indices = {
            0: "AC",
            1: "AM",
            2: "PA",
            3: "AP",
            4: "TO",
            5: "MA",
            6: "PI",
            7: "CE",
            8: "RN",
            9: "PB",
            10: "PE",
            11: "AL",
            12: "SE",
            13: "BA",
            14: "MG",
            15: "ES",
            16: "RJ",
            17: "SP",
            18: "PR",
            19: "SC",
            20: "RS",
            21: "MS",
            22: "MT",
            23: "GO",
            24: "DF",
            25: "RO",
            26: "RR",
        }
        print("Estado:", estados_indices[state_clicked])
        return estados_indices[state_clicked]

    @app.callback(
        [Output(f"btn-ano-{ano}", "style") for ano in anos],
        [Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
    )
    def update_button_styles(*n_clicks):
        ctx = dash.callback_context

        # Identificar o ano selecionado
        ano_selecionado = anos[0]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-ano" in prop_id:
                ano_selecionado = int(
                    prop_id.split(".")[0].split("-")[-1]
                )  # Extrai o ano do ID do botão

        # Atualizar o estilo dos botões com base no ano selecionado
        estilos = []
        for ano in anos:
            if ano == ano_selecionado:
                estilo = {
                    "background-color": "#000000",  # Fundo preto
                    "border-color": "#A5A5A5",  # Cor da borda
                    "color": "#fff",  # Cor do texto
                    "padding": "0px 12px",
                }
            else:
                estilo = {
                    "background-color": "#A5A5A5",  # Fundo cinza claro
                    "border-color": "#A5A5A5",  # Cor da borda
                    "color": "#fff",  # Cor do texto
                    "padding": "0px 12px",
                }
            estilos.append(estilo)
        return estilos
