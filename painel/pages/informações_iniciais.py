import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from callbacks.api_requests import get_anos

from components.map import Map

dash.register_page(__name__, path="/")

anos = get_anos(6)

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

slash_column = dbc.Col([
        html.Span(
            style={
                "display": "inline-block",
                "width": "1px",
                "height": "100%",
                "background-color": "#212529bf",
            }
        )
    ], className="slash")

def  indicator_component(title, ind_brasil, ind_estado, ind, icon): 
    legend = html.Div([])

    if ind_brasil != None:
        legend = html.Div(
            className="indicator-legend-box",
            children=[
                html.Div(
                className="indicator-legend",
                children=[
                    square_legend,
                    html.P(
                        id=ind_brasil,
                        className="legend-text"
                    ),
                ]),
                html.Div(
                    className="indicator-legend",
                    children=[
                    rhombus_legend,
                    html.P(
                        id=ind_estado,
                        className="legend-text"
                    ),
                ]),
            ]
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
                        html.Div([
                            html.Span(className=f"fa fa-{icon}", style={"color": "white", "font-size": "10px"})
                        ], className="icon-content")
                    ]
                ),
            )
        ],
        className="indicator-column"
    )

layout = html.Div(
    [
        html.Div(
          id="indicators",

          children=[
            Map(),
            html.Div([
                html.H2(
                    "Panorama geral",
                    id="overview",
                ),
                html.Div (
                  id="indicator-content",
                  children=[
                    html.H2(
                        "Atendimentos individuais",
                        id="atendimentos-title",
                    ),
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
                                className="legend-text"
                            ),
                        ]),
                        html.Div(
                            className="indicator-legend",
                            children=[
                            rhombus_legend,
                            html.P(
                                "Estado",
                                className="legend-text"
                            ),
                        ]),
                    ]),
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
                                className="indicator-column"
                            ),
                            slash_column,
                            dbc.Col(
                                [
                                    dbc.Row(
                                        html.H4(
                                            "Atendimentos por mil hab. no ano",
                                            className="description-indicator",
                                        ),
                                    ),
                                    html.Div(
                                        className="indicator-legend-box",
                                        children=[
                                            html.Div(
                                            className="indicator-legend",
                                            children=[
                                                square_legend,
                                                html.P(
                                                    id="indicador-atend-brasil",
                                                    className="legend-text"
                                                ),
                                            ]),
                                            html.Div(
                                                className="indicator-legend",
                                                children=[
                                                rhombus_legend,
                                                html.P(
                                                    id="indicador-atend-estado",
                                                    className="legend-text"
                                                ),
                                            ]),
                                        ]
                                    ),
                                    dbc.Row(
                                        html.H2(
                                            id="normalizado-atendimentos",
                                            className="indicator-number",
                                        ),
                                    ),
                                ],
                                className="px-4 indicator-column"
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
                                "tooth"
                            ),
                            slash_column,
                            indicator_component(
                                "Atendimentos feitos em visita domiciliar",
                                "indicador-visita-brasil",
                                "indicador-visita-estado",
                                "big-visitas",
                                "house"
                            ),
                            slash_column,
                            indicator_component(
                                "Atendimentos feitos por médicos",
                                None,
                                None,
                                "big-medicos",
                                "user-doctor"

                            ),
                            slash_column,
                            indicator_component(
                                "Encaminhamentos",
                                None,
                                None,
                                "big-encaminhamentos",
                                "hand-point-right"
                            )
                        ],
                        className="mb-1",
                    ),
                  ]
                ),
            ], style={"width": "100%"}),
          ]
        ),


        html.H2(
            "Visão ao decorrer do tempo",
            id="overview",
            className="mt-3"
        ),
        html.Div (
            id="year-content",
            className="time-visualization-content",
            children=[
                dbc.Row([
                    dbc.Col(
                        [
                            html.H2(
                                "Atendimentos por mil habitantes",
                                id="atendimentos-title",
                            ),
                            dcc.Graph(
                                id="chart_by_year",
                                style={"height": "35vh"},
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H2(
                                "Encaminhamentos",
                                id="atendimentos-title",
                            ),
                            dcc.Graph(
                                id="chart_encaminhamentos",
                                style={"height": "35vh"},
                            ),
                        ]
                    )
                ]),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2(
                                    "Atendimentos odontológicos",
                                    id="atendimentos-title",
                                ),
                                dcc.Graph(
                                    id="chart_odonto_by_year",
                                    style={"height": "35vh"},
                                ),
                            ]
                        ),
                        dbc.Col(   
                            [
                                html.H2(
                                    "Atendimentos feitos em visita domiciliar",
                                    id="atendimentos-title",
                                ),
                                dcc.Graph(
                                    id="chart_visitas_by_year",
                                    style={"height": "35vh"},
                                ),
                            ]
                        ),
                        dbc.Col(   
                            [
                                html.H2(
                                    "Atendimentos por profissionais",
                                    id="atendimentos-title",
                                ),
                                dcc.Graph(
                                    id="chart_by_year_profissionais",
                                    style={"height": "35vh"},
                                ),
                            ]
                        ),
                    ],
                ),
            ]
        ),
        html.Div( 
            id="quarter-content",
            className="time-visualization-content",
            children=[
                dbc.Row(
                    [
                        dbc.Col([
                            html.H2(
                                "Atendimentos por mil habitantes",
                                id="atendimentos-title",
                            ),
                            dcc.Graph(
                                id="chart_by_quarter",
                                style={"height": "35vh"},
                            ),
                        ]),
                        dbc.Col(),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col([
                            html.H2(
                                "Atendimentos odontológicos",
                                id="atendimentos-title",
                            ),
                            dcc.Graph(
                                id="chart_odonto_by_quarter",
                                style={"height": "35vh"},
                            ),
                        ]),
                        dbc.Col([
                            html.H2(
                                "Atendimentos feitos em visita domiciliar",
                                id="atendimentos-title",
                            ),
                            dcc.Graph(
                                id="chart_visitas_by_quarter",
                                style={"height": "35vh"},
                            ),
                        ]),
                    ],
                ),
            ]
        ),
    ],
    style={"padding": "0px 25px"},
)
