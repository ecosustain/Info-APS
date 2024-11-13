import time

from dash import Input, Output, no_update
from callbacks.utils.utils import get_type


def callback(app):
    @app.callback(
        Output("loading-graphics", "display", allow_duplicate=True),
        Input("loading-graphics", "display"),
        allow_duplicate=True,
        prevent_initial_call=True
    )
    def loading_trigger(value):
        if (value == "show"):
            time.sleep(2.5)
            return "hide"
        return no_update
    
    @app.callback(
        Output("loading-graphics", "color"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
    )
    def loading_trigger(estado, regiao, municipio):
        tipo = get_type(estado, regiao, municipio)
        
        style_loading= {
            "brasil": "#632956",
            "estado": "#34679A",
            "regiao":  "#2B7B6F",
            "municipio": "#F7941C",
        }

        return style_loading[tipo]

            

