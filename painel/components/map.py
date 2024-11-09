import dash_bootstrap_components as dbc
from dash import dcc, html


def Map():
    return dbc.Row(
        [
            dcc.Graph(
                config={
                    "displayModeBar": False,
                    "scrollZoom": False,
                },
                id="mapa",
                style={"height": "300px", "width": "520px"},
            ),
            html.Div(id="output-state"),  # Div para mostrar o estado clicado
        ],
        className="mb-1",
    )
