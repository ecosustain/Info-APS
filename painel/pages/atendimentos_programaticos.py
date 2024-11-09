import dash
import dash_bootstrap_components as dbc
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
                    "Atendimentos individuais",
                    id="atendimentos-title",
                ),
                html.Div (
                  id="indicator-content",
                  children=[
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
                        className="mb-3",
                    ),
                  ]
                ),
            ], style={"width": "100%"}),
          ]
        ),
        dbc.Row(
            [
                indicator_component(
                    "Enfermeiros",
                    None,
                    None,
                    "big-enfermeiros",
                    "user-nurse"
                ),
            ]
        ),
        dbc.Row(
            [
                # Hipertensão por população por ano
                dbc.Col(
                    dcc.Graph(
                        id="chart_hipertensao_by_year",
                        style={"height": "40vh"},
                    ),
                    width=3,
                ),  
                # Hipertensão por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_hipertensao_by_quarter",
                        style={"height": "40vh"},
                    ),
                    width=9,
                ),  
                dbc.Col(),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Diabetes por população por ano
                dbc.Col(
                    dcc.Graph(
                        id="chart_diabetes_by_year",
                        style={"height": "40vh"},
                    ),
                    width=3,
                ),  
                # Diabetes por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_diabetes_by_quarter",
                        style={"height": "40vh"},
                    ),
                    width=9,
                ),  
                dbc.Col(),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Saude Sexual por população por ano
                dbc.Col(
                    dcc.Graph(
                        id="chart_saude_sexual_by_year",
                        style={"height": "40vh"},
                    ),
                    width=3,
                ),  
                # Saude Sexual por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_saude_sexual_by_quarter",
                        style={"height": "40vh"},
                    ),
                    width=9,
                ),  
                dbc.Col(),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Saude Mental por população por ano
                dbc.Col(
                    dcc.Graph(
                        id="chart_saude_mental_by_year",
                        style={"height": "40vh"},
                    ),
                    width=3,
                ),  
                # Saude Mental por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_saude_mental_by_quarter",
                        style={"height": "40vh"},
                    ),
                    width=9,
                ),  
                dbc.Col(),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Puericultura por população por ano
                dbc.Col(
                    dcc.Graph(
                        id="chart_puericultura_by_year",
                        style={"height": "40vh"},
                    ),
                    width=3,
                ),  
                # Puericultura por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_puericultura_by_quarter",
                        style={"height": "40vh"},
                    ),
                    width=9,
                ),  
                dbc.Col(),
            ],
            className="mb-3",
        ),
    ]
)
