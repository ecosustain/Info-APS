"""Módulo HTML para a página de atendimentos totais."""

import dash
import dash_bootstrap_components as dbc
from api.api_requests import anos
from components.chart_component import chart_component
from components.geometric_elements import rhombus_legend, square_legend
from components.indicator_component import indicator_component
from components.map import Map
from components.slash_column import slash_column
from dash import dcc, html

dash.register_page(__name__, path="/")
dash.register_page(
    __name__,
    path="/",
    title="Atendimentos Totais",
    name="Atendimentos Totais",
    order=1
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
                                                dbc.Col(
                                                    [
                                                        html.P(
                                                            "Total",
                                                            className="description-indicator-total",
                                                        ),
                                                        html.H2(
                                                            id="total-atendimentos",
                                                            className="indicator-number-total",
                                                        ),
                                                    ],
                                                    className="indicator-column",
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Atendimentos por mil hab. no ano",
                                                    "indicador-atend-brasil",
                                                    "indicador-atend-estado",
                                                    "normalizado-atendimentos",
                                                    None,
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Atendimentos feitos por médicos",
                                                    None,
                                                    None,
                                                    "big-medicos",
                                                    "user-doctor",
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "% de Encaminhamentos",
                                                    None,
                                                    None,
                                                    "big-encaminhamentos",
                                                    "hand-point-right",
                                                ),
                                            ],
                                            className="mb-4",
                                        ),
                                        dbc.Row(
                                            [
                                                indicator_component(
                                                    "Atendimentos odontológicos",
                                                    "indicador-odont-brasil",
                                                    "indicador-odont-estado",
                                                    "big-odontologicos",
                                                    "tooth",
                                                ),
                                                slash_column,
                                                indicator_component(
                                                    "Atendimentos feitos em visita domiciliar",
                                                    "indicador-visita-brasil",
                                                    "indicador-visita-estado",
                                                    "big-visitas",
                                                    "house",
                                                ),
                                            ],
                                            className="mb-1",
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
                                    "Atendimentos Totais",
                                    "chart_by_year",
                                    "por mil habitantes",
                                ),
                                chart_component(
                                    "Encaminhamentos",
                                    "chart_encaminhamentos",
                                    "% atendimentos totais",
                                    "hand-point-right",
                                ),
                                chart_component(
                                    "Atendimentos por profissionais",
                                    "chart_by_year_profissionais",
                                    "por mil habitantes",
                                    "user-doctor",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos odontológicos",
                                    "chart_odonto_by_year",
                                    "por mil habitantes",
                                    "tooth",
                                ),
                                chart_component(
                                    "Atendimentos feitos em visita domiciliar",
                                    "chart_visitas_by_year",
                                    "por mil habitantes",
                                    "house",
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
                                    "Atendimentos por mil habitantes",
                                    "chart_by_quarter",
                                    "por mil habitantes",
                                ),
                            ],
                            className="content-chart-wrapper",
                        ),
                        dbc.Row(
                            [
                                chart_component(
                                    "Atendimentos odontológicos",
                                    "chart_odonto_by_quarter",
                                    "por mil habitantes",
                                    "tooth",
                                ),
                                chart_component(
                                    "Atendimentos feitos em visita domiciliar",
                                    "chart_visitas_by_quarter",
                                    "por mil habitantes",
                                    "house",
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
                "padding-bottom": "175px",
            },
            color="#632956",
            type="circle",
        ),
    ],
    style={"padding": "200px 25px 50px 25px"},
)
