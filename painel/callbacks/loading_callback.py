"""Módulo para callbacks do loading."""

import time

from dash import Input, Output, no_update, clientside_callback


def callback(app):
    """Função para registrar os callbacks do loading."""

    clientside_callback(
        """
        function(value) {
            if (value == "show") {
                setTimeout(3000)
                return "hide"
            }

            if (value == "auto") return "show"
            
            return dash_clientside.no_update
        }
        """,
        Output("loading-graphics", "display"),
        Input("loading-graphics", "display"),
    )

    clientside_callback(
        """
        function(estado, regiao, municipio, style) {
            if (municipio) {
                return "#F7941C"
            }
            if (regiao) {
                return "#2B7B6F"
            }
            if (estado) {
                return "#34679A"
            }
            return "#632956"
        }
        """,
        Output("loading-graphics", "color"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
        Input("loading-graphics", "style"),
    )
