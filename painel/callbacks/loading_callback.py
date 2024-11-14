import time
import dash

from callbacks.utils.utils import get_type
from dash import Input, Output, no_update


def callback(app):
    def loading_trigger(id):
        @app.callback(
            Output(id, "display", allow_duplicate=True),
            Input(id, "display"),
            allow_duplicate=True,
            prevent_initial_call=True,
        )
        def loading_trigger(value):
            if value == "show":
                time.sleep(2.5)
                return "hide"
            return no_update
    
    loading_trigger("loading-graphics")
    loading_trigger("loading-page")

    @app.callback(
        Output("loading-graphics", "color"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
    )
    def loading_trigger(estado, regiao, municipio):
        tipo = get_type(estado, regiao, municipio)

        style_loading = {
            "brasil": "#632956",
            "estado": "#34679A",
            "regiao": "#2B7B6F",
            "municipio": "#F7941C",
        }

        return style_loading[tipo]
