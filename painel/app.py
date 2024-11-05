import dash
import dash_bootstrap_components as dbc
from callbacks.api_requests import get_anos
from callbacks.callbacks import register_callbacks
from callbacks.utils import estados_brasileiros
from dash import dcc, html

# Inicializa a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


anos = get_anos(6)

# Layout da aplicação
app.layout = dbc.Container(
    [  # Add dropdown of states here
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="dropdown-estado",
                        options=[
                            {"label": estado, "value": estado}
                            for estado in estados_brasileiros
                        ],
                        placeholder="Selecione o Estado",
                        searchable=True,
                        clearable=True,  # Permite limpar a seleção
                    ),
                    width=2,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="dropdown-regiao",
                        options=[],
                        placeholder="Selecione a Região",
                        searchable=True,
                        clearable=True,  # Permite limpar a seleção
                    ),
                    width=4,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="dropdown-municipio",
                        options=[],
                        placeholder="Selecione o Municipio",
                        searchable=True,
                        clearable=True,  # Permite limpar a seleção
                    ),
                    width=4,
                ),
            ]
        ),
        dbc.Row(
            # breakline
            html.Br(),
        ),
        dbc.Row(
            dbc.Col(
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
                            className="me-4 rounded",  # Adiciona margem à direita e borda arredondada
                            style={
                                "background-color": (
                                    "#A5A5A5" if ano != anos[0] else "#000000"
                                ),  # Fundo cinza claro ou escuro
                                "border-color": "#A5A5A5",  # Cor da borda
                                "color": (
                                    "#fff" if ano != anos[0] else "#00000"
                                ),  # Cor do texto
                                "padding": "0px 12px",
                            },
                        )
                        for ano in anos
                    ],
                    vertical=False,  # Para deixar os botões lado a lado
                )
            ),
            className="mb-4",
        ),
        dbc.Row(
            [
                dcc.Graph(
                    config={"displayModeBar": False, "scrollZoom": False},
                    id="mapa",
                    style={"height": "40vh"},
                ),
                html.Div(
                    id="output-state"
                ),  # Div para mostrar o estado clicado
            ],
            className="mb-1",
        ),
        dcc.Store(id="store-data"),
        dcc.Store(id="store-data-enc"),
        dcc.Store(id="store-data-visita"),
        dcc.Store(id="store-data-odonto"),
        dcc.Store(id="store-populacao"),
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
                        html.H2(
                            id="normalizado-atendimentos",
                            className="display-8 text-start fw-bold",
                        ),
                        html.H4(
                            "Número de atendimentos por mil habitantes no ano",
                            className="fs-6 text-muted",
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
                    dbc.Row(
                        [
                            # Coluna do ícone
                            dbc.Col(
                                html.Img(
                                    src="assets/tooth-solid.svg", height="25px"
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
                ),
                dbc.Col(
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
                                    src="assets/user-solid.svg", height="25px"
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
                    dcc.Graph(id="chart_by_year", style={"height": "40vh"}),
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
                    dcc.Graph(id="chart_by_quarter", style={"height": "40vh"}),
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
                        id="chart_encaminhamentos", style={"height": "40vh"}
                    ),
                    width=6,
                ),  # Segunda coluna com o gráfico
            ],
            className="mb-3",
        ),
        dbc.Row(
            html.H3(
                "Visitas Domiciliar",
                className="text-start ms-0, mb-3",
                id="section-visitas",
            )
        ),
        dbc.Row(
            [
                # Atendimento por visitas domiciliar por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_visitas_by_quarter", style={"height": "40vh"}
                    ),
                    width=12,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            html.H3(
                "Atendimentos Odontologicos",
                className="text-start ms-0, mb-3",
                id="section-odontologicos",
            )
        ),
        dbc.Row(
            [
                # Atendimento por atendimentos odontologicos por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_odonto_by_quarter", style={"height": "40vh"}
                    ),
                    width=12,
                ),
            ],
            className="mb-3",
        ),
        html.Div(id="dummy-div", children=[], style={"display": "none"}),
    ],
    className="p-3 mx-auto",
    style={"max-width": "80%"},
)

# Inicializa os callbacks
register_callbacks(app)


# Rodar o servidor
if __name__ == "__main__":
    app.run(
        debug=True,
        dev_tools_silence_routes_logging=False,
        dev_tools_prune_errors=False,
        dev_tools_hot_reload=False,
    )
