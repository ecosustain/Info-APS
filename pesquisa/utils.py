import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd

cadastro = pd.read_csv("../etl/data/consolidado/Cadastro.csv")
condicao = pd.read_csv("../etl/data/consolidado/producao_problema.csv")
ano = 2023
cadastro_uf = (
    cadastro[(cadastro["Ano"] == ano) & (cadastro["Mes"] == "DEZ")][
        ["Uf", "Cadastros"]
    ]
    .groupby("Uf")
    .sum()
)
procedimentos = pd.read_csv(
    "../etl/data/consolidado/producao_procedimento.csv"
)

# Convertendo as colunas numéricas para inteiros
colunas_numerica = [col for col in procedimentos.columns if procedimentos[col].dtype == 'float64']
procedimentos[colunas_numerica] = procedimentos[colunas_numerica].astype(int)
colunas_numerica = [col for col in condicao.columns if condicao[col].dtype == 'float64']
condicao[colunas_numerica] = condicao[colunas_numerica].astype(int)

# Carregar o shapefile do Brasil
brasil = gpd.read_file('../mapas/BR_UF_2022/BR_UF_2022.shp')
brasil['geometry'] = brasil['geometry'].simplify(0.1)

def get_condicao_normalizada(coluna, ano):
    """Função que retorna a condição normalizada por 100 mil habitantes"""
    df_condicao = (
        condicao[condicao["Ano"] == ano][["Uf", coluna]].groupby("Uf").sum()
    )
    df_condicao_norm = round(
        df_condicao[coluna] / (cadastro_uf["Cadastros"] / 100000), 2
    )
    df_condicao_norm = pd.DataFrame(df_condicao_norm).reset_index()
    df_condicao_norm.columns = ["Uf", "value"]
    return df_condicao_norm


def plot_map(brasil, df, title):
    """Função que plota o mapa coroplético com base nos dados normalizados"""
    # Merge do shapefile com os dados
    brasil = brasil.merge(df, left_on="SIGLA_UF", right_on="Uf", how="left")
    # drop column Uf
    brasil = brasil.drop(columns="Uf")
    # Criar o mapa coroplético
    fig = px.choropleth(
        brasil,
        geojson=brasil.geometry,
        locations=brasil.index,
        color="value",
        hover_data={"NM_UF": False, "value": True},
        hover_name="NM_UF",
        title=title,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        height=600,
        width=700,
        coloraxis_colorbar=dict(
            title="Atend p/ <br>100k Hab",
        ),
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Valor: %{z:,.0f}<extra></extra>"
    )
    fig.show()


def get_prevencao_secundaria(estado, municipio, colunas):
    """Função para obter os dados de prevenção primária de um município"""
    colunas = colunas + ["Ano"]
    if municipio is not None:
        proc = procedimentos[
            (procedimentos["Municipio"] == municipio)
            & (procedimentos["Uf"] == estado)
        ][colunas]
        proc = proc.groupby("Ano").sum().sum(axis=1)
        return proc.to_json()
    if estado is not None:
        proc = procedimentos[procedimentos["Uf"] == estado][colunas]
        proc = proc.groupby("Ano").sum().sum(axis=1)
        return proc.to_json()
    if estado is None and municipio is None:
        proc = procedimentos[colunas]
        proc = proc.groupby("Ano").sum().sum(axis=1)
        return proc.to_json()
    return None


def get_doencas_prevencao(estado, municipio, colunas):
    """Função para obter os dados de prevenção primária de um município"""
    colunas = colunas + ["Ano"]
    if municipio is not None:
        proc = condicao[
            (condicao["Municipio"] == municipio) & (condicao["Uf"] == estado)
        ][colunas]
        proc = proc.groupby("Ano").sum().sum(axis=1)
        return proc.to_json()
    if estado is not None:
        proc = condicao[condicao["Uf"] == estado][colunas]
        proc = proc.groupby("Ano").sum().sum(axis=1)
        return proc.to_json()
    if estado is None and municipio is None:
        proc = condicao[colunas]
        proc = proc.groupby("Ano").sum().sum(axis=1)
        return proc.to_json()
    return None


def comparativo_doenca_procedimento(procedimento, doenca, titulo):
    # Convertendo as strings JSON para dicionários
    proc_prev_dict = json.loads(procedimento)
    doencas_prev_dict = json.loads(doenca)

    # Criando as figuras
    fig = go.Figure()

    # Adicionando o gráfico de procedimentos de prevenção secundária
    fig.add_trace(
        go.Bar(
            x=list(proc_prev_dict.keys()),
            y=list(proc_prev_dict.values()),
            name=f"Prevenção",
        )
    )

    # Adicionando o gráfico de doenças de prevenção secundária
    fig.add_trace(
        go.Bar(
            x=list(doencas_prev_dict.keys()),
            y=list(doencas_prev_dict.values()),
            name=f"Condição",
        )
    )

    # Atualizando o layout para exibir os gráficos lado a lado e mover a legenda para o topo
    fig.update_layout(
        barmode="group",
        title=titulo,
        xaxis_title="Ano",
        yaxis_title="Quantidade",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
    )
    fig.update_traces(hovertemplate="Valor: %{y:,.0f}<extra></extra>")

    fig.show()


def dataframe_razao(procedimentos_filtro, condicao_filtro, titulo):
    estados = [
        "AC",
        "AL",
        "AM",
        "AP",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MG",
        "MS",
        "MT",
        "PA",
        "PB",
        "PE",
        "PI",
        "PR",
        "RJ",
        "RN",
        "RO",
        "RR",
        "RS",
        "SC",
        "SE",
        "SP",
        "TO",
    ]
    dict_estados = {}
    for estado in estados:
        if titulo == "Gravidez":
            proc_prev = get_doencas_prevencao(
                estado, None, procedimentos_filtro
            )
        else:
            proc_prev = get_prevencao_secundaria(
                estado, None, procedimentos_filtro
            )
        doencas_prev = get_doencas_prevencao(estado, None, condicao_filtro)

        proc_prev_dict = json.loads(proc_prev)
        doencas_prev_dict = json.loads(doencas_prev)
        # Filtrar dados a partir de 2016
        proc_prev_dict = {
            ano: proc_prev_dict[ano]
            for ano in proc_prev_dict
            if int(ano) >= 2016
        }
        doencas_prev_dict = {
            ano: doencas_prev_dict[ano]
            for ano in doencas_prev_dict
            if int(ano) >= 2016
        }
        divisao_dict = {}
        for ano in proc_prev_dict:
            divisao_dict[ano] = proc_prev_dict[ano] / doencas_prev_dict[ano]
        dict_estados[estado] = divisao_dict
    dict_estados
    # Criando o DataFrame com as colunas Uf, Ano e Value
    df = pd.DataFrame(columns=["Uf", "Ano", "Value"])
    # Iterando sobre o dicionário de estados
    for uf, divisao_dict in dict_estados.items():
        # Iterando sobre os anos
        for ano, value in divisao_dict.items():
            # Adicionando a linha ao DataFrame
            df = df.append(
                {"Uf": uf, "Ano": ano, "Value": value}, ignore_index=True
            )
    return df


def get_geojson_data(df):
    brasil_razao = brasil.merge(df, left_on="SIGLA_UF", right_on="Uf")
    geojson_data = brasil_razao.__geo_interface__

    return brasil_razao, geojson_data


def mapa_razao(brasil_razao, geojson_data, titulo):
    # Calcular
    percentil = brasil_razao["Value"].quantile(0.95)
    percentil = round(percentil, 3)
    # Criar um gráfico coroplético animado por ano
    fig = px.choropleth(
        brasil_razao,
        geojson=geojson_data,  # GeoJSON criado a partir do GeoDataFrame
        locations="SIGLA_UF",  # Coluna com siglas dos estados
        color="Value",  # Coluna de valores que serão representados
        featureidkey="properties.SIGLA_UF",
        hover_name="NM_UF",  # Nome do estado ao passar o cursor
        animation_frame="Ano",  # Coluna que define o ano para a animação
        color_continuous_scale="Viridis",  # Escala de cores
        range_color=(0, percentil),
        title=f"Razao entre Prevenção e Condição de {titulo}",
    )

    # Atualizar o layout para centralizar o mapa no Brasil
    fig.update_geos(fitbounds="locations", visible=False)

    # Atualizar a legenda das cores
    fig.update_layout(
        height=600,
        width=700,
        coloraxis_colorbar=dict(
            title="Razão",
        ),
    )

    # Mostrar o gráfico
    fig.show()


def gera_mapa(procedimentos_filtro, condicao_filtro, titulo):
    df = dataframe_razao(procedimentos_filtro, condicao_filtro, titulo)
    brasil_razao, geojson_data = get_geojson_data(df)
    mapa_razao(brasil_razao, geojson_data, titulo)
