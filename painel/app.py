import dash
import dash_bootstrap_components as dbc

from callbacks.api_requests import get_anos
from callbacks.callbacks import register_callbacks
from callbacks.callbacks_visita_domiciliar import register_callbacks_visita
from callbacks.callbacks_atendimentos_odonto import register_callbacks_odonto

from dash import dcc, html

from components.sidebar_structure import SideBar
from components.header import Header
from components.map import Map

# Inicializa a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

anos = get_anos(6)

# Layout da aplicação
app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        # dbc.Col(html.Div(id="page-content"), width=10),
        # Add dropdown of states here
        dbc.Row(
            [
                SideBar(),
                html.Div(
                    id="content",
                    children=[
                        Header(),
                        Map(),
                        dcc.Store(id="store-data"),
                        dcc.Store(id="store-data-enc"),
                        dcc.Store(id="store-data-visita"),
                        dcc.Store(id="store-data-odonto"),
                        dcc.Store(id="store-populacao"),
                        dcc.Store(id="nivel-geo"),
                        # Menu em abas
                        dash.page_container,
                    ],
                    style={"left": "0", "padding": "200px 12px 0px 232px", "background-color": "#F8F9FA"},
                ),
                html.Div(
                    id="dummy-div", children=[], style={"display": "none"}
                ),
            ]
        ),
    ],
    className="p-0 mx-auto",
    style={"max-width": "100%"},
)

# Inicializa os callbacks
register_callbacks(app)
register_callbacks_visita(app)
register_callbacks_odonto(app)

# Rodar o servidor
if __name__ == "__main__":
    app.run(
        debug=True,
        dev_tools_silence_routes_logging=False,
        dev_tools_prune_errors=False,
        dev_tools_hot_reload=False,
    )
