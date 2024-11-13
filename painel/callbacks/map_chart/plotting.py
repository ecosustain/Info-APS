"""Módulo para gerar mapas interativos com Plotly Express"""

import geopandas as gpd
import pandas as pd
import plotly.express as px
from callbacks.utils.utils import get_regioes, municipios


def remove_internal_polygons(gdf, estado):
    """Função para remover polígonos internos e manter apenas as bordas"""
    # Adiciona a regiao e o no_regiao
    mun = gdf["NM_MUN"][0].upper()

    regiao = municipios[
        (municipios["uf"] == estado) & (municipios["municipio"] == mun)
    ]["regiao"].values[0]
    no_regiao = municipios[
        (municipios["uf"] == estado) & (municipios["municipio"] == mun)
    ]["no_regiao"].values[0]

    polygon = gdf.geometry.union_all()

    gdf2 = gpd.GeoDataFrame(geometry=[polygon], crs=gdf.crs)
    gdf2["regiao"] = regiao
    gdf2["no_regiao"] = no_regiao

    return gdf2


def get_shapefile_regiao(estado):
    """Função para obter o shapefile de um estado"""
    regioes = get_regioes(estado)
    # regioes unicas
    regioes = list(set(regioes.keys()))

    return [
        f"mapas/shapefiles/{estado}/{regiao}/{regiao}.shp"
        for regiao in regioes
    ]


def get_mapa_brasil():
    """Função para criar o mapa do Brasil"""
    shapefile_uf = "mapas/BR_UF_2022/BR_UF_2022.shp"
    brasil_estados = gpd.read_file(shapefile_uf)
    mapa_uf = brasil_estados[["SIGLA_UF", "geometry"]]
    mapa_uf["geometry"] = brasil_estados["geometry"].simplify(tolerance=0.01)
    mapa_uf["value"] = 1
    fig = px.choropleth(
        mapa_uf,
        geojson=mapa_uf.geometry,  # Usar a geometria do shapefile
        locations=mapa_uf.index,  # Nome da coluna do DataFrame
        hover_name="SIGLA_UF",
        hover_data={"SIGLA_UF": False, "value": False},
        color="value",
        color_continuous_scale=[
            "#632956",
            "#632956",
            "#632956",
        ],
    )

    # Ajustar as configurações do mapa
    fig.update_geos(
        fitbounds="locations",
        visible=False,
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=False,
        dragmode=False,
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><extra></extra>",
        hoverlabel=dict(
            bgcolor="#343A40",
            font_color="white",
            font_size=12,
            bordercolor="#343A40",
        ),
        marker_line_color="white",
        marker_line_width=0.5,
    )

    return fig


def get_mapa_estado(estado):
    """Função para plotar os shapefiles de um estado"""
    shapefiles = get_shapefile_regiao(estado)

    # Carregar múltiplos shapefiles
    dataframes = [gpd.read_file(path) for path in shapefiles]
    # remove internal polygons with list comprehension
    dataframes = [remove_internal_polygons(df, estado) for df in dataframes]

    # Combinar os DataFrames em um único DataFrame
    combined_df = gpd.GeoDataFrame(pd.concat(dataframes, ignore_index=True))
    combined_df["value"] = 1

    # simplificar a geometria
    combined_df["geometry"] = combined_df["geometry"].simplify(tolerance=0.01)

    # Criar o gráfico
    fig = px.choropleth(
        combined_df,
        geojson=combined_df.geometry,
        locations=combined_df.index,
        hover_name="no_regiao",  # Supondo que todos os shapefiles têm essa coluna
        hover_data={"value": False},
        color="value",
        color_continuous_scale=["#34679A", "#34679A", "#34679A"],
    )

    # Ajustar as configurações do mapa
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=False,
        dragmode=False,
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><extra></extra>",
        hoverlabel=dict(
            bgcolor="#343A40",
            font_color="white",
            font_size=12,
            bordercolor="#343A40",
        ),
        marker_line_color="white",
        marker_line_width=0.5,
    )

    return fig


def get_mapa_regiao(estado, regiao):
    """Função para criar o mapa de um estado"""
    if type(regiao) is not int and not regiao.isnumeric():
        regioes = get_regioes(estado)
        # get the key by value
        regiao = list(regioes.keys())[list(regioes.values()).index(regiao)]

    shapefile = f"mapas/shapefiles/{estado}/{regiao}/{regiao}.shp"

    mapa_mun = gpd.read_file(shapefile)
    mapa_mun = mapa_mun[["CD_MUN", "NM_MUN", "SIGLA_UF", "geometry"]]
    mapa_mun["geometry"] = mapa_mun["geometry"].simplify(tolerance=0.001)
    mapa_mun["value"] = 1

    fig = px.choropleth(
        mapa_mun,
        geojson=mapa_mun.geometry,  # Usar a geometria do shapefile
        locations=mapa_mun.index,  # Nome da coluna do DataFrame
        hover_name="NM_MUN",
        hover_data={
            "SIGLA_UF": False,
            "value": False,
        },
        color="value",
        color_continuous_scale=[
            "#2B7B6F",
            "#2B7B6F",
            "#2B7B6F",
        ],
    )

    # Ajustar as configurações do mapa
    fig.update_geos(
        fitbounds="locations",
        visible=False,
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=False,
        dragmode=False,
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><extra></extra>",
        hoverlabel=dict(
            bgcolor="#343A40",
            font_color="white",
            font_size=12,
            bordercolor="#343A40",
        ),
        marker_line_color="white",
        marker_line_width=0.5,
    )

    return fig


def get_mapa_municipio(estado, municipio):
    """Função para criar o mapa de um município"""
    shapefile = f"mapas/Estados/{estado}/{estado}_Municipios_2022.shp"

    mapa_mun = gpd.read_file(shapefile)
    # Transformar nome do município em maiúsculas
    mapa_mun["NM_MUN"] = mapa_mun["NM_MUN"].str.upper()
    mapa_mun = mapa_mun[mapa_mun["NM_MUN"] == municipio]
    mapa_mun = mapa_mun[["CD_MUN", "NM_MUN", "SIGLA_UF", "geometry"]]
    # mapa_mun["geometry"] = mapa_mun["geometry"].simplify(tolerance=0.001)
    mapa_mun["value"] = 1

    fig = px.choropleth(
        mapa_mun,
        geojson=mapa_mun.geometry,  # Usar a geometria do shapefile
        locations=mapa_mun.index,  # Nome da coluna do DataFrame
        hover_name="NM_MUN",
        hover_data={
            "SIGLA_UF": False,
            "value": False,
        },
        color="value",
        color_continuous_scale=[
            "#F7941C",
            "#F7941C",
            "#F7941C",
        ],
    )

    # Ajustar as configurações do mapa
    fig.update_geos(
        fitbounds="locations",
        visible=False,
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=False,
        dragmode=False,
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><extra></extra>",
        hoverlabel=dict(
            bgcolor="#343A40",
            font_color="white",
            font_size=12,
            bordercolor="#343A40",
        ),
        marker_line_color="white",
        marker_line_width=0.5,
    )

    return fig
