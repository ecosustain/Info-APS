"""Módulo com os callbacks da página Principal"""
import json

import dash
import dash.dependencies as dd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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


df_atendimentos = get_df_atendimentos(json_data)
# df_altas = get_df_altas(json_data)
anos = [2024, 2023, 2022, 2021, 2020, 2019]


def register_callbacks(app):
    # Callback para atualizar o número de atendimentos
    @app.callback(
        [
            dd.Output("total-atendimentos", "children"),
            dd.Output("big-medicos", "children"),
            dd.Output("big-enfermeiros", "children"),
            dd.Output("big-outros", "children"),
        ],
        [
            dd.Input(f"btn-{ano}", "n_clicks") for ano in anos
        ],  # Um input para cada botão de ano
        [
            dd.State(f"btn-{ano}", "id") for ano in anos
        ],  # Para pegar o ID do botão clicado
    )
    def update_big_numbers(*args):
        # Função para atualizar os números grandes
        ctx = dash.callback_context
        if not ctx.triggered or ctx.triggered[0]["prop_id"] == ".":
            ano = anos[0]  # Define o primeiro ano como padrão
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            ano = int(button_id.split("-")[1])  # Extrai o ano do ID do botão

        # Pegar os números grandes
        big_numbers = get_big_numbers_atendimentos(df_atendimentos, ano)

        # dividir cada big number por 1000 para facilitar a leitura
        big_numbers = [int(num / 100000) for num in big_numbers]

        return big_numbers

    get_chart_by_quarter, get_chart_by_year_profissionais, get_chart_by_year

    # Callback para atualizar os gráficos de atendimentos
    @app.callback(
        [
            dd.Output("chart_by_year", "figure"),
            dd.Output("chart_by_year_profissionais", "figure"),
            dd.Output("chart_by_quarter", "figure"),
        ],
        [
            dd.Input(f"btn-{ano}", "n_clicks") for ano in anos
        ],  # Um input para cada botão de ano
        [
            dd.State(f"btn-{ano}", "id") for ano in anos
        ],  # Para pegar o ID do botão clicado
    )
    def update_charts(*args):
        # Função para atualizar os gráficos
        ctx = dash.callback_context
        if not ctx.triggered or ctx.triggered[0]["prop_id"] == ".":
            ano = anos[0]  # Define o primeiro ano como padrão
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            ano = int(button_id.split("-")[1])  # Extrai o ano do ID do botão

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
