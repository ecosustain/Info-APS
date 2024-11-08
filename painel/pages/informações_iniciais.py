import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        dbc.Row(
            html.H2(
                "Atendimentos",
                className="text-start ms-0, mb-4",
                id="section-atendimentos",
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            id="total-atendimentos",
                            className="display-8 text-start fw-bold",
                        ),
                        html.H4(
                            "Total de atendimentos individuais",
                            className="fs-6 text-muted",
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(width=1),  # Coluna vazia para espaçamento
                dbc.Col(
                    [
                        dbc.Row(
                            html.H2(
                                id="normalizado-atendimentos",
                                className="display-8 text-start fw-bold",
                            ),
                        ),
                        dbc.Row(
                            html.H4(
                                "Número de atendimentos por mil habitantes no ano",
                                className="fs-6 text-muted",
                            ),
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Span(
                                            style={
                                                "display": "inline-block",
                                                "width": "13px",
                                                "height": "13px",
                                                "background-color": "#632956",
                                                "margin-right": "5px",
                                            }
                                        ),
                                        html.H6(
                                            id="indicador-atend-brasil",
                                            style={
                                                "margin-bottom": "0",
                                                "font-size": "14px",
                                            },
                                        ),
                                    ],
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                    },
                                ),
                                dbc.Col(
                                    [
                                        html.Span(
                                            style={
                                                "display": "inline-block",
                                                "width": "13px",
                                                "height": "13px",
                                                "background-color": "#34679A",
                                                "transform": "rotate(45deg)",
                                                "margin-right": "5px",
                                            }
                                        ),
                                        html.H6(
                                            id="indicador-atend-estado",
                                            style={
                                                "margin-bottom": "0",
                                                "font-size": "14px",
                                            },
                                        ),
                                    ],
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                    },
                                ),
                            ]
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(width=1),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Span(
                                        style={
                                            "display": "inline-block",
                                            "width": "15px",
                                            "height": "15px",
                                            "background-color": "#632956",
                                            "margin-right": "5px",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    html.H5(
                                        "Brasil",
                                        style={
                                            "margin-bottom": "0",
                                        },
                                    ),
                                    width=2,
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Span(
                                        style={
                                            "display": "inline-block",
                                            "width": "15px",
                                            "height": "15px",
                                            "background-color": "#34679A",
                                            "transform": "rotate(45deg)",
                                            "margin-right": "5px",
                                        }
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    html.H5(
                                        "Estado",
                                        style={
                                            "margin-bottom": "0",
                                        },
                                    ),
                                    width=2,
                                ),
                            ],
                        ),
                    ],
                    width=3,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                # Coluna do ícone
                                dbc.Col(
                                    html.Img(
                                        src="assets/tooth-solid.svg",
                                        height="25px",
                                    ),
                                    width="auto",
                                ),
                                # Coluna do número
                                dbc.Col(
                                    html.H3(
                                        id="big-odontologicos",
                                        className="display-8 fw-bold mb-0",
                                    ),
                                    width="auto",
                                ),
                            ],
                            align="center",
                        ),
                        dbc.Row(
                            [
                                # Coluna do texto, com ajuste de tamanho
                                dbc.Col(
                                    html.P(
                                        [
                                            "Atendimentos",
                                            html.Br(),
                                            "odontológicos",
                                        ],
                                        className="text-muted",
                                        style={
                                            "font-size": "14px",
                                            "margin-bottom": "0",
                                            "align-self": "flex-end",
                                        },
                                    ),
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "align-items": "flex-end",
                                    },  # Para alinhar o texto ao final do número
                                ),
                            ],
                            align="center",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Span(
                                            style={
                                                "display": "inline-block",
                                                "width": "10px",
                                                "height": "10px",
                                                "background-color": "#632956",
                                            }
                                        ),
                                        html.P(
                                            id="indicador-odont-brasil",
                                            style={
                                                "margin-bottom": "0",
                                                "margin-left": "2px",
                                                "margin-right": "2px",
                                                "font-size": "12px",
                                            },
                                        ),
                                    ],
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                    },
                                ),
                                dbc.Col(
                                    [
                                        html.Span(
                                            style={
                                                "display": "inline-block",
                                                "width": "10px",
                                                "height": "10px",
                                                "background-color": "#34679A",
                                                "transform": "rotate(45deg)",
                                            }
                                        ),
                                        html.P(
                                            id="indicador-odont-estado",
                                            style={
                                                "margin-bottom": "0",
                                                "margin-left": "2px",
                                                "margin-right": "2px",
                                                "font-size": "12px",
                                            },
                                        ),
                                    ],
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                    },
                                ),
                            ]
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                # Coluna do ícone
                                dbc.Col(
                                    html.Img(
                                        src="assets/house-solid.svg",
                                        height="25px",
                                    ),
                                    width="auto",
                                ),
                                # Coluna do número
                                dbc.Col(
                                    html.H3(
                                        id="big-visitas",
                                        className="display-8 fw-bold mb-0",
                                    ),
                                    width="auto",
                                ),
                                # Coluna do texto, com ajuste de tamanho
                                dbc.Col(
                                    html.P(
                                        [
                                            "Atendimentos feitos",
                                            html.Br(),
                                            "em visita domiciliar",
                                        ],
                                        className="text-muted",
                                        style={
                                            "font-size": "14px",
                                            "margin-bottom": "0",
                                            "align-self": "flex-end",
                                        },
                                    ),
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "align-items": "flex-end",
                                    },  # Para alinhar o texto ao final do número
                                ),
                            ],
                            align="center",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Span(
                                            style={
                                                "display": "inline-block",
                                                "width": "10px",
                                                "height": "10px",
                                                "background-color": "#632956",
                                            }
                                        ),
                                        html.P(
                                            id="indicador-visita-brasil",
                                            style={
                                                "margin-bottom": "0",
                                                "margin-left": "2px",
                                                "margin-right": "2px",
                                                "font-size": "12px",
                                            },
                                        ),
                                    ],
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                    },
                                ),
                                dbc.Col(
                                    [
                                        html.Span(
                                            style={
                                                "display": "inline-block",
                                                "width": "10px",
                                                "height": "10px",
                                                "background-color": "#34679A",
                                                "transform": "rotate(45deg)",
                                            }
                                        ),
                                        html.P(
                                            id="indicador-visita-estado",
                                            style={
                                                "margin-bottom": "0",
                                                "margin-left": "2px",
                                                "margin-right": "2px",
                                                "font-size": "12px",
                                            },
                                        ),
                                    ],
                                    width="auto",
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                    },
                                ),
                            ]
                        ),
                    ],
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            # Coluna do ícone
                            dbc.Col(
                                html.Img(
                                    src=dash.get_asset_url(
                                        "user-doctor-solid.svg"
                                    ),
                                    height="25px",
                                ),
                                width="auto",
                            ),
                            # Coluna do número
                            dbc.Col(
                                html.H3(
                                    id="big-medicos",
                                    className="display-8 fw-bold mb-0",
                                ),
                                width="auto",
                            ),
                            # Coluna do texto, com ajuste de tamanho
                            dbc.Col(
                                html.P(
                                    [
                                        "Atendimentos feitos",
                                        html.Br(),
                                        "por médicos",
                                    ],
                                    className="text-muted",
                                    style={
                                        "font-size": "14px",
                                        "margin-bottom": "0",
                                        "align-self": "flex-end",
                                    },
                                ),
                                width="auto",
                                style={
                                    "display": "flex",
                                    "align-items": "flex-end",
                                },  # Para alinhar o texto ao final do número
                            ),
                        ],
                        align="center",
                    ),
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            # Coluna do ícone
                            dbc.Col(
                                html.Img(
                                    src="assets/user-nurse-solid.svg",
                                    height="25px",
                                ),
                                width="auto",
                            ),
                            # Coluna do número
                            dbc.Col(
                                html.H3(
                                    id="big-enfermeiros",
                                    className="display-8 fw-bold mb-0",
                                ),
                                width="auto",
                            ),
                            # Coluna do texto, com ajuste de tamanho
                            dbc.Col(
                                html.P(
                                    [
                                        "Atendimentos feitos",
                                        html.Br(),
                                        "por enfermeiros",
                                    ],
                                    className="text-muted",
                                    style={
                                        "font-size": "14px",
                                        "margin-bottom": "0",
                                        "align-self": "flex-end",
                                    },
                                ),
                                width="auto",
                                style={
                                    "display": "flex",
                                    "align-items": "flex-end",
                                },  # Para alinhar o texto ao final do número
                            ),
                        ],
                        align="center",
                    ),
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            # Coluna do ícone
                            dbc.Col(
                                html.Img(
                                    src="assets/user-solid.svg",
                                    height="25px",
                                ),
                                width="auto",
                            ),
                            # Coluna do número
                            dbc.Col(
                                html.H3(
                                    id="big-encaminhamentos",
                                    className="display-8 fw-bold mb-0",
                                ),
                                width="auto",
                            ),
                            # Coluna do texto, com ajuste de tamanho
                            dbc.Col(
                                html.P(
                                    [
                                        "Atendimentos finalizados",
                                        html.Br(),
                                        "com encaminhamento",
                                    ],
                                    className="text-muted",
                                    style={
                                        "font-size": "14px",
                                        "margin-bottom": "0",
                                        "align-self": "flex-end",
                                    },
                                ),
                                width="auto",
                                style={
                                    "display": "flex",
                                    "align-items": "flex-end",
                                },  # Para alinhar o texto ao final do número
                            ),
                        ],
                        align="center",
                    ),
                ),
            ],
            className="mb-5",
        ),
        dbc.Row(
            [
                # Atendimento por população por ano
                dbc.Col(
                    dcc.Graph(
                        id="chart_by_year",
                        style={"height": "40vh"},
                    ),
                    width=6,
                ),  # Primeira coluna com o gráfico
                # Atendimento por profissional de saúde
                # dbc.Col(
                #     dcc.Graph(
                #         id="chart_by_year_profissionais",
                #         style={"height": "40vh"},
                #     ),
                #     width=6,
                # ),  # Segunda coluna com o gráfico
                dbc.Col(),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Atendimento poe população por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_by_quarter",
                        style={"height": "40vh"},
                    ),
                    width=12,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H3(
                        "Profissionais",
                        className="text-start ms-0, mb-3",
                        id="section-profissionais",
                    )
                ),
                dbc.Col(
                    html.H3(
                        "Encaminhamentos",
                        className="text-start ms-0, mb-3",
                        id="section-encaminhamentos",
                    )
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Atendimento por profissional de saúde
                dbc.Col(
                    dcc.Graph(
                        id="chart_by_year_profissionais",
                        style={"height": "40vh"},
                    ),
                    width=6,
                ),  # Primeira coluna com o gráfico
                # Atendimento por encaminhamento
                dbc.Col(
                    dcc.Graph(
                        id="chart_encaminhamentos",
                        style={"height": "40vh"},
                    ),
                    width=6,
                ),  # Segunda coluna com o gráfico
            ],
            className="mb-3",
        ),
    ],
    style={"padding": "5px 5px"},
)
