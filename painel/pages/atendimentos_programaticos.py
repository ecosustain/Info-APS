"""Módulo para página de atendimentos programáticos"""

import dash
import dash_bootstrap_components as dbc
from callbacks.api_requests import anos
from dash import dcc, html

dash.register_page(
    __name__,
    path="/atendimentos-programaticos",
    title="Programáticos",
    name="Programáticos",
)

from components.map import Map

square_legend = html.Span(
    style={
        "display": "inline-block",
        "width": "8px",
        "height": "8px",
        "background-color": "#632956",
        "margin-right": "5px",
    }
)

rhombus_legend = html.Span(
    style={
        "display": "inline-block",
        "width": "8px",
        "height": "8px",
        "background-color": "#34679A",
        "transform": "rotate(45deg)",
        "margin-right": "5px",
    }
)

slash_column = dbc.Col(
    [
        html.Span(
            style={
                "display": "inline-block",
                "width": "1px",
                "height": "100%",
                "background-color": "#212529bf",
            }
        )
    ],
    className="slash",
)


def indicator_component(title, ind_brasil, ind_estado, ind):
    legend = html.Div([])

    if ind_brasil != None:
        legend = html.Div(
            className="indicator-legend-box",
            children=[
                html.Div(
                    className="indicator-legend",
                    children=[
                        square_legend,
                        html.P(id=ind_brasil, className="legend-text"),
                    ],
                ),
                html.Div(
                    className="indicator-legend",
                    children=[
                        rhombus_legend,
                        html.P(id=ind_estado, className="legend-text"),
                    ],
                ),
            ],
        )

    return dbc.Col(
        [
            dbc.Row(
                html.H4(
                    title,
                    className="description-indicator-small",
                ),
            ),
            legend,
            dbc.Row(
                html.Div(
                    className="indicator-footer",
                    children=[
                        html.H2(
                            id=ind,
                            className="indicator-number-small",
                        ),
                    ],
                ),
            ),
        ],
        className="indicator-column",
    )


layout = html.Div(
    [
        html.Div(
            id="indicators",
            children=[
                Map(),
                html.Div(
                    [
                        html.H2(
                            "Atendimentos Programáticos",
                            id="atendimentos-title",
                        ),
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
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Diabetes",
                                            "indicador-diabetes-brasil",
                                            "indicador-diabetes-estado",
                                            "big-diabetes",
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Saúde Sexual",
                                            "indicador-sexual-brasil",
                                            "indicador-sexual-estado",
                                            "big-sexual",
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
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Puericultura",
                                            "indicador-puericultura-brasil",
                                            "indicador-puericultura-estado",
                                            "big-puericultura",
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Grávidas",
                                            "indicador-gravidas-brasil",
                                            "indicador-gravidas-estado",
                                            "big-gravidas",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                            ],
                        ),
                    ],
                    style={"width": "100%"},
                ),
            ],
        ),
        html.H2("Visão ao decorrer do tempo", id="overview", className="mt-3"),
        html.Div(
            id="year-content",
            className="time-visualization-content",
            children=[
                dbc.Row(
                    [
                        # Hipertensão por população por ano
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Hipertensão Arterial",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_hipertensao_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Diabetes por população por ano
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Diabetes",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_diabetes_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Saude Sexual por população por ano
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Saúde Sexual",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_saude_sexual_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # Saude Mental por população por ano
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Saúde Mental",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_saude_mental_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Puericultura por população por ano
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Puericultura",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_puericultura_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Gravidez por população por ano
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Gravidez Adequados",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_gravidez_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="quarter-content",
            className="time-visualization-content",
            children=[
                dbc.Row(
                    [
                        # Hipertensão por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Hipertensão Arterial",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_hipertensao_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                        # Diabetes por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Diabetes",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_diabetes_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # Saude Sexual por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Saúde Sexual",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_saude_sexual_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                        # Saude Mental por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Saúde Mental",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_saude_mental_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # Puericultura por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Puericultura",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_puericultura_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                        # Gravidez por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos adequados de Gravidez",
                                    className="description-indicator",
                                ),
                                dcc.Graph(
                                    id="chart_gravidez_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
            ],
        ),
    ],
)
