import dash
import dash_bootstrap_components as dbc
from callbacks.api_requests import get_anos, anos
from callbacks.callbacks import register_callbacks
from callbacks.callbacks_atendimentos_odonto import register_callbacks_odonto
from callbacks.callbacks_visita_domiciliar import register_callbacks_visita
from callbacks.callbacks_programaticos import register_callbacks_programaticos
from components.header import Header
from components.sidebar_structure import SideBar
from dash import dcc, html


# Inicializa a aplicação Dash
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v6.4.2/css/all.css"], use_pages=True, 
)

# Layout da aplicação
app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        # dbc.Col(html.Div(id="page-content"), width=10),
        # Add dropdown of states here
        html.Div(
            [
                SideBar(),
                html.Div(
                    id="content",
                    children=[
                        Header(),
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
                        # Menu em abas
                        dash.page_container,
                    ],
                    style={
                        "left": "0",
                        "padding": "200px 12px 0px 232px",
                        "background-color": "#F8F9FA",
                    },
                ),
                html.Div(
                    id="dummy-div", children=[], style={"display": "none"}
                ),
            ],
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

# Rodar o servidor
if __name__ == "__main__":
    app.run(
        debug=True,
        dev_tools_silence_routes_logging=False,
        dev_tools_prune_errors=False,
        dev_tools_hot_reload=False,
        host="0.0.0.0"
    )
