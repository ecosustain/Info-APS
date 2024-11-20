"""Módulo para a página de atendimentos não programáticos"""

import dash
import dash_bootstrap_components as dbc
from api.api_requests import anos
from components.chart_component import chart_component
from components.geometric_elements import rhombus_legend, square_legend
from components.indicator_component import indicator_component
from components.map import Map
from components.slash_column import slash_column
from dash import dcc, html

dash.register_page(
    __name__,
    path="/atendimentos-nao-programaticos",
    title="Atendimentos Não Programáticos",
    name="Atendimentos Não Programáticos",
)

layout = html.Div(
    [
        dcc.Loading(
            [
                html.Div(
                    id="indicators",
                    children=[
                        Map(),
                        html.Div(
                            [
                                html.Div(
                                    id="indicator-content",
                                    children=[
                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    str(ano),
                                                    id=f"btn-ano-{ano}",
                                                    color="primary",
                                                    outline=True,
                                                    active=(
                                                        ano == anos[0]
                                                    ),  # Define o primeiro ano como ativo
                                                    className="year-button rounded",
                                                )
                                                for ano in anos
                                            ],
                                            vertical=False,  # Para deixar os botões lado a lado
                                        ),
                                        html.Div(
                                            className="indicator-legend-box",
                                            children=[
                                                html.Div(
                                                    className="indicator-legend",
                                                    children=[
                                                        square_legend,
                                                        html.P(
                                                            "Brasil",
                                                            className="legend-text",
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="indicator-legend",
                                                    children=[
                                                        rhombus_legend,
                                                        html.P(
                                                            "Estado",
                                                            className="legend-text",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Row(
                                            [
                                                indicator_component(
                                                    "ASMA e DPOC",
                                                    "indicador-asma-dpoc-brasil",
                                                    "indicador-asma-dpoc-estado",
                                                    "big-asma-dpoc",
                                                    None,
                                                    ""
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Dengue",
                                                    "indicador-dengue-brasil",
                                                    "indicador-dengue-estado",
                                                    "big-dengue",
                                                    None,
                                                    ""
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Tuberculose",
                                                    "indicador-tuberculose-brasil",
                                                    "indicador-tuberculose-estado",
                                                    "big-tuberculose",
                                                    None,
                                                    ""
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                indicator_component(
                                                    "IST",
                                                    "indicador-dst-brasil",
                                                    "indicador-dst-estado",
                                                    "big-dst",
                                                    None,
                                                    ""
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Hanseníase",
                                                    "indicador-hanseniase-brasil",
                                                    "indicador-hanseniase-estado",
                                                    "big-hanseniase",
                                                    None,
                                                    ""
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Febres",
                                                    "indicador-febres-brasil",
                                                    "indicador-febres-estado",
                                                    "big-febres",
                                                    None,
                                                    ""
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                indicator_component(
                                                    "Cefaléia",
                                                    "indicador-cefaleia-brasil",
                                                    "indicador-cefaleia-estado",
                                                    "big-cefaleia",
                                                    None,
                                                    ""
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Tosse",
                                                    "indicador-tosse-brasil",
                                                    "indicador-tosse-estado",
                                                    "big-tosse",
                                                    None,
                                                    ""
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.H2(
                    "Série Temporal ",
                    id="overview",
                    className="mt-3",
                ),
                html.Div(
                    id="year-content",
                    className="time-visualization-content",
                    children=[
                        html.Div(
                            html.Span(
                                "Ano",
                                id="tag-ano",
                                className="tag rounded",
                            ),
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Asma e DPOC",
                                    "chart_asma_dpoc_by_year",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Dengue",
                                    "chart_dengue_by_year",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Tuberculose",
                                    "chart_tuberculose_by_year",
                                    "por 100 mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de IST",
                                    "chart_dst_by_year",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Hanseníase",
                                    "chart_hanseniase_by_year",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Febres",
                                    "chart_febres_by_year",
                                    "por 100 mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Cefaleia",
                                    "chart_cefaleia_by_year",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Tosse",
                                    "chart_tosse_by_year",
                                    "por 100 mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                    ],
                ),
                html.Div(
                    id="quarter-content",
                    className="time-visualization-content",
                    children=[
                        html.Div(
                            html.Span(
                                "Trimestre",
                                id="tag-trimestre",
                                className="tag rounded",
                            ),
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Asma e DPOC",
                                    "chart_asma_dpoc_by_quarter",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Dengue",
                                    "chart_dengue_by_quarter",
                                    "por 100 mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Tuberculose",
                                    "chart_tuberculose_by_quarter",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de IST",
                                    "chart_dst_by_quarter",
                                    "por 100 mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Hanseníase",
                                    "chart_hanseniase_by_quarter",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Febres",
                                    "chart_febres_by_quarter",
                                    "por 100 mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Cefaleia",
                                    "chart_cefaleia_by_quarter",
                                    "por 100 mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Tosse",
                                    "chart_tosse_by_quarter",
                                    "por 100 mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                    ],
                ),
            ],
            id="loading-graphics",
            overlay_style={
                "visibility": "visible",
                "filter": "blur(2px)",
            },
            style={
                "height": "100%",
                "position": "fixed",
                "display": "flex",
                "padding-top": "25vh",
            },
            color="#632956",
            type="circle",
        )
    ],
    style={"padding": "200px 25px 50px 25px"},
)
