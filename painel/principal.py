import dash
import dash_bootstrap_components as dbc
from callbacks.principal_callbacks import anos, register_callbacks
from dash import dcc, html

# Inicializa a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

estados_brasileiros = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]



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
                        id="dropdown-cidade",
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
                dcc.Graph(id="mapa"),
                html.Div(
                    id="output-state"
                ),  # Div para mostrar o estado clicado
            ]
        ),
        dcc.Store(id="store-data"),
        dcc.Store(id="store-populacao"),
        html.Div(id="dummy-div", children=[], style={"display": "none"}),
        dbc.Row(
            html.H1(
                "Atendimentos",
                className="text-start ms-0, mb-4",
                id="section-atendimentos",
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            id="total-atendimentos",
                            className="display-6 text-start fw-bold",
                        ),
                        html.H4(
                            "Número de atendimentos individuais \
                                já registrados",
                            className="fs-6",
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(width=1),  # Coluna vazia para espaçamento
                dbc.Col(
                    [
                        html.H1(
                            id="normalizado-atendimentos",
                            className="display-6 text-start fw-bold",
                        ),
                        html.H4(
                            "Número de atendimentos por mil habitantes no ano",
                            className="fs-6",
                        ),
                    ],
                    width=3,
                ),
            ],
            className="mb-5",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Row(
                        [
                            # Coluna do ícone
                            dbc.Col(
                                html.Img(
                                    src=dash.get_asset_url("medico-icon.png"),
                                    height="25px",
                                ),
                                width="auto",
                            ),
                            # Coluna do número
                            dbc.Col(
                                html.H3(
                                    id="big-medicos",
                                    className="display-6 fw-bold",
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
                                    style={
                                        "font-size": "12px",
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
                    width=4,
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            # Coluna do ícone
                            dbc.Col(
                                html.Img(
                                    src="assets/enfermeiro-icon.png",
                                    height="25px",
                                ),
                                width="auto",
                            ),
                            # Coluna do número
                            dbc.Col(
                                html.H1(
                                    id="big-enfermeiros",
                                    className="display-6 fw-bold",
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
                                    style={
                                        "font-size": "12px",
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
                    width=4,
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            # Coluna do ícone
                            dbc.Col(
                                html.Img(
                                    src="assets/outros-icon.png", height="25px"
                                ),
                                width="auto",
                            ),
                            # Coluna do número
                            dbc.Col(
                                html.H1(
                                    id="big-outros",
                                    className="display-6 fw-bold",
                                ),
                                width="auto",
                            ),
                            # Coluna do texto, com ajuste de tamanho
                            dbc.Col(
                                html.P(
                                    [
                                        "Atendimentos feitos",
                                        html.Br(),
                                        "por outros profissionais",
                                    ],
                                    style={
                                        "font-size": "12px",
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
                    width=4,
                ),
            ]
        ),
        dbc.Row(
            [
                # Atendimento por população por ano
                dbc.Col(
                    dcc.Graph(id="chart_by_year", style={"height": "400px"}),
                    width=6,
                ),  # Primeira coluna com o gráfico
                # Atendimento por profissional de saúde
                dbc.Col(
                    dcc.Graph(
                        id="chart_by_year_profissionais",
                        style={"height": "400px"},
                    ),
                    width=6,
                ),  # Segunda coluna com o gráfico
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                # Atendimento poe população por trimestre
                dbc.Col(
                    dcc.Graph(
                        id="chart_by_quarter", style={"height": "400px"}
                    ),
                    width=12,
                ),
            ],
            className="mb-4",
        ),
        dcc.Store(id="store-data-altas"),
        dbc.Row(
            html.H1(
                "Altas", className="text-start ms-0, mb-4", id="section-altas"
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            id="total-altas",
                            className="display-6 text-start fw-bold",
                        ),
                        html.H4(
                            "Número total de altas \
                                registradas",
                            className="fs-6",
                        ),
                    ],
                    width=3,
                ),
            ],
            className="mb-5",
        ),
        dbc.Row(
            [
                # Atendimento por população por ano
                dbc.Col(
                    dcc.Graph(id="chart_altas", style={"height": "400px"}),
                    width=6,
                ),  # Primeira coluna com o gráfico
                # Atendimento por profissional de saúde
                dbc.Col(),  # Segunda coluna com o gráfico
            ],
            className="mb-4",
        ),
        dcc.Store(id="store-data-enc"),
        dbc.Row(
            html.H1(
                "Encaminhamentos",
                className="text-start ms-0, mb-4",
                id="section-encaminhamentos",
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            id="total-encaminhamentos",
                            className="display-6 text-start fw-bold",
                        ),
                        html.H4(
                            "Número total de encaminhamentos \
                                registrados",
                            className="fs-6",
                        ),
                    ],
                    width=3,
                ),
            ],
            className="mb-5",
        ),
        dbc.Row(
            [
                # Atendimento por população por ano
                dbc.Col(
                    dcc.Graph(
                        id="chart_encaminhamentos", style={"height": "400px"}
                    ),
                    width=6,
                ),  # Primeira coluna com o gráfico
                # Atendimento por profissional de saúde
                dbc.Col(),  # Segunda coluna com o gráfico
            ],
            className="mb-4",
        ),
    ],
    className="p-5 mx-auto",
    style={"max-width": "80%"},
)

# Inicializa os callbacks
register_callbacks(app)


# Rodar o servidor
if __name__ == "__main__":
    app.run() # port=8050, debug=True, dev_tools_silence_routes_logging=False, dev_tools_prune_errors=False, dev_tools_hot_reload=False)
