from callbacks.utils.utils import get_type
from dash import Input, Output


def callback(app):
    def update_button_style_template(id, style):
        @app.callback(
            Output(id, "style"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        )
        def update_button_style(estado, regiao, municipio):

            tipo = get_type(estado, regiao, municipio)

            return style[tipo]

    style_by_type_indicators = {
        "brasil": {
            "color": "#632956",
            "background-color": "#6329561a",
            "border": "1px solid #632956",
        },
        "estado": {
            "color": "#34679A",
            "background-color": "#34679A1a",
            "border": "1px solid #34679A",
        },
        "regiao": {
            "color": "#2B7B6F",
            "background-color": "#2B7B6F1a",
            "border": "1px solid #2B7B6F",
        },
        "municipio": {
            "color": "#F7941C",
            "background-color": "#F7941C1a",
            "border": "1px solid #F7941C",
        },
    }

    ids=[
        "indicator-icon-tooth",
        "indicator-icon-house",
        "indicator-icon-user-doctor",
        "indicator-icon-hand-point-right",
        "tag-trimestre",
        "tag-ano",
    ]

    for id in ids:
        update_button_style_template(id, style_by_type_indicators)