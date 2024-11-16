"""Módulo com o layout do mapa"""

import dash_bootstrap_components as dbc
from dash import dcc, html


def Map():
    """Função para retornar o layout do mapa"""
    return dbc.Row(
        [
            dcc.Graph(
                config={
                    "displayModeBar": False,
                    "scrollZoom": False,
                },
                id="mapa",
                style={"height": "300px", "width": "520px"},
                clear_on_unhover=True,
            ),
            html.Div(id="output-state"),  # Div para mostrar o estado clicado
        ],
        className="mb-1",
    )
