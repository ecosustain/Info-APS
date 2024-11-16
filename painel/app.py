"""Módulo principal da aplicação."""

import os

import dash
import dash_bootstrap_components as dbc
from callbacks.callbacks import register_callbacks
from callbacks.callbacks_atendimentos_odonto import register_callbacks_odonto
from callbacks.callbacks_nao_programaticos import register_callbacks_nao_programaticos
from callbacks.callbacks_programaticos import register_callbacks_programaticos
from callbacks.callbacks_visita_domiciliar import register_callbacks_visita
from components.header import Header
from components.footer import Footer
from components.sidebar_structure import SideBar
from dash import dcc, html

# Inicializa a aplicação Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://use.fontawesome.com/releases/v6.4.2/css/all.css",
    ],
    use_pages=True,
)

# Layout da aplicação
app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        # dbc.Col(html.Div(id="page-content"), width=10),
        # Add dropdown of states here
        html.Div(
            id="platform",
            children=[
                SideBar(),
                html.Div(
                    id="content",
                    children=[
                        Header(),
                        dcc.Store(id="store-populacao-api"),
                        dcc.Store(id="store-data"),
                        dcc.Store(id="store-data-enc"),
                        dcc.Store(id="store-data-visita"),
                        dcc.Store(id="store-data-odonto"),
                        dcc.Store(id="store-populacao"),
                        dcc.Store(id="nivel-geo"),
                        # Programático
                        dcc.Store(id="store-data-hipertensao"),
                        dcc.Store(id="store-data-diabetes"),
                        dcc.Store(id="store-data-saude-sexual"),
                        dcc.Store(id="store-data-saude-mental"),
                        dcc.Store(id="store-data-puericultura"),
                        dcc.Store(id="store-data-gravidez-adequado"),
                        dcc.Store(id="store-data-gravidez-inadequado"),
                        # Não Programático
                        dcc.Store(id="store-data-asma-dpoc"),
                        dcc.Store(id="store-data-dengue"),
                        dcc.Store(id="store-data-tuberculose"),
                        dcc.Store(id="store-data-dst"),
                        dcc.Store(id="store-data-hanseniase"),
                        dcc.Store(id="store-data-cefaleia"),
                        dcc.Store(id="store-data-tosse"),
                        dcc.Store(id="store-data-febres"),
                        # Menu em abas
                        dash.page_container,
                        Footer(),
                    ],
                    style={
                        "left": "0",
                        "padding-left": "220px",
                        "background-color": "#F8F9FA",
                        "min-height": "100vh",
                    },
                ),
                html.Div(
                    id="dummy-div", children=[], style={"display": "none"}
                ),
            ],
        ),
        html.Div(
            id="only-desktop",
            children=[
                html.Div(
                    [
                        html.H2(
                            "É preciso um dispositvo maior",
                            className="message-screen",
                        ),
                        html.P(
                            "tente em um dispositivo com mais de 860 pixels de largura",
                            className="message-description",
                        ),
                        html.Span(
                            className="fa fa-heart-crack icon-message",
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "align-items": "center",
                        "margin": "20px",
                    },
                )
            ],
            style={
                "background-color": "#343A40",
            },
        ),
    ],
    className="p-0 mx-auto",
    style={"max-width": "100%"},
)

# Inicializa os callbacks
register_callbacks(app)
register_callbacks_visita(app)
register_callbacks_odonto(app)
register_callbacks_programaticos(app)
register_callbacks_nao_programaticos(app)

# Rodar o servidor
if __name__ == "__main__":
    host = os.getenv(
        "HOST", "127.0.0.1"
    )  # Usar variável de ambiente para configurar o host
    port = os.getenv(
        "PORT", 8050
    )  # Usar variável de ambiente para configurar a porta
    app.run_server(
        debug=True,
        dev_tools_silence_routes_logging=False,
        dev_tools_prune_errors=False,
        dev_tools_hot_reload=False,
        host=host,
        port=port,
    )
