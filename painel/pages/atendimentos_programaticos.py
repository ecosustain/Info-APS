"""Módulo para página de atendimentos programáticos"""

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
    path="/atendimentos-programaticos",
    title="Atendimentos Programáticos",
    name="Atendimentos Programáticos",
)


square_legend = html.Span(
    style={
        "display": "inline-block",
        "width": "8px",
        "height": "8px",
        "background-color": "#632956",
        "margin-right": "5px",
    }
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
                                                    "Hipertensão Arterial",
                                                    "indicador-hipertensao-brasil",
                                                    "indicador-hipertensao-estado",
                                                    "big-hipertensao",
                                                    None,
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Diabetes",
                                                    "indicador-diabetes-brasil",
                                                    "indicador-diabetes-estado",
                                                    "big-diabetes",
                                                    None,
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Saúde Sexual",
                                                    "indicador-sexual-brasil",
                                                    "indicador-sexual-estado",
                                                    "big-sexual",
                                                    None,
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                indicator_component(
                                                    "Saúde Mental",
                                                    "indicador-mental-brasil",
                                                    "indicador-mental-estado",
                                                    "big-mental",
                                                    None,
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Puericultura",
                                                    "indicador-puericultura-brasil",
                                                    "indicador-puericultura-estado",
                                                    "big-puericultura",
                                                    None,
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Gravidez Adequada",
                                                    "indicador-gravidas-brasil",
                                                    "indicador-gravidas-estado",
                                                    "big-gravidas",
                                                    None,
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ],
                ),
                html.H2(
                    "Série Temporal ",
                    id="overview",
                    className="mt-4",
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
                                    "Atendimentos de Hipertensão Arterial",
                                    "chart_hipertensao_by_year",
                                    "por mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Diabetes",
                                    "chart_diabetes_by_year",
                                    "por mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Saúde Sexual",
                                    "chart_saude_sexual_by_year",
                                    "por mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Saúde Mental",
                                    "chart_saude_mental_by_year",
                                    "por mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Puericultura",
                                    "chart_puericultura_by_year",
                                    "por mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Gravidez Adequados",
                                    "chart_gravidez_by_year",
                                    "% atendimentos de gravidez",
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
                                    "Atendimentos de Hipertensão Arterial",
                                    "chart_hipertensao_by_quarter",
                                    "por mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Diabetes",
                                    "chart_diabetes_by_quarter",
                                    "por mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Saúde Sexual",
                                    "chart_saude_sexual_by_quarter",
                                    "por mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos de Saúde Mental",
                                    "chart_saude_mental_by_quarter",
                                    "por mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos de Puericultura",
                                    "chart_puericultura_by_quarter",
                                    "por mil habitantes",
                                ),
                                chart_component(
                                    "Atendimentos adequados de Gravidez",
                                    "chart_gravidez_by_quarter",
                                    "% atendimentos de gravidez",
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
