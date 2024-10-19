import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from callbacks.principal_callbacks import anos, register_callbacks
from dash import dcc, html

# Inicializa a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout da aplicação
app.layout = dbc.Container(
    [  # Add dropdown of states here
        dbc.Row(
            dbc.Col(
                dbc.DropdownMenu(
                    label="Selecione o Estado",
                    children=[
                        dbc.DropdownMenuItem("São Paulo", id="dropdown-sp"),
                        dbc.DropdownMenuItem(
                            "Rio de Janeiro", id="dropdown-rj"
                        ),
                        dbc.DropdownMenuItem("Minas Gerais", id="dropdown-mg"),
                    ],
                ),
                width=3,
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            str(ano),
                            id=f"btn-{ano}",
                            color="primary",
                            outline=True,
                            active=(
                                ano == anos[0]
                            ),  # Define o primeiro ano como ativo
                            className="me-4 rounded",  # Adiciona margem à direita e borda arredondada
                            style={
                                "background-color": "#A5A5A5"
                                if ano != anos[0]
                                else "#000000",  # Fundo cinza claro ou escuro
                                "border-color": "#A5A5A5",  # Cor da borda
                                "color": "#fff"
                                if ano != anos[0]
                                else "#00000",  # Cor do texto
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
        dbc.Row(html.H1("Atendimentos", className="text-start ms-0, mb-4")),
        dbc.Row(
            [  # 2 colunas. Cada coluna com o número grande em cima e embaixo a descrição
                dbc.Col(
                    [
                        html.H1(
                            id="total-atendimentos",
                            className="display-6 text-start fw-bold",
                        ),
                        html.H4(
                            "Número de atendimentos individuais já registrados",
                            className="fs-6",
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(width=1),  # Coluna vazia para espaçamento
                dbc.Col(
                    [
                        html.H1("4", className="display-6 text-start fw-bold"),
                        html.H4(
                            "Número de atendimentos por pessoa no ano de 2023",
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
                            # Coluna do texto, com ajuste de tamanho e alinhamento
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
                            # Coluna do texto, com ajuste de tamanho e alinhamento
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
                            # Coluna do texto, com ajuste de tamanho e alinhamento
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
                    dcc.Graph(id="chart_by_year"), width=6
                ),  # Primeira coluna com o gráfico
                # Atendimento por profissional de saúde
                dbc.Col(
                    dcc.Graph(id="chart_by_year_profissionais"), width=6
                ),  # Segunda coluna com o gráfico
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                # Atendimento poe população por trimestre
                dbc.Col(dcc.Graph(id="chart_by_quarter"), width=10),
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
    app.run_server(debug=True)
