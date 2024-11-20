"""Módulo para callbacks do loading."""

import time

from callbacks.utils.utils import get_type
from dash import Input, Output, no_update


def callback(app):
    """Função para registrar os callbacks do loading."""

    @app.callback(
        Output("loading-graphics", "display", allow_duplicate=True),
        Input("loading-graphics", "display"),
        allow_duplicate=True,
        prevent_initial_call=True,
    )
    def loading_trigger(value):
        """Função para atualizar o loading"""
        if value == "show":
            time.sleep(2.5)
            return "hide"
        return no_update


    @app.callback(
        Output("loading-graphics", "color"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
        Input("loading-graphics", "style"),
    )
    def loading_trigger_2(estado, regiao, municipio, style):
        tipo = get_type(estado, regiao, municipio)

        style_loading = {
            "brasil": "#632956",
            "estado": "#34679A",
            "regiao": "#2B7B6F",
            "municipio": "#F7941C",
        }

        return style_loading[tipo]
    