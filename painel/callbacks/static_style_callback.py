from dash import Output, Input

from callbacks.utils.utils import get_type

def callback(app):
    def  update_button_style_template(id):
        @app.callback(
            Output(id, "style"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        )
        def update_button_style(estado, regiao, municipio):
            
            tipo = get_type(estado, regiao, municipio)
            
            style_by_type= {
                "brasil": {
                    "color": "#632956",
                    "font-size": "10px",
                    "padding": "5px",
                    "border-radius": "50%",
                    "background-color": "#6329561a",
                    "border": "1px solid #632956"
                },
                "estado": {
                    "color": "#34679A",
                    "font-size": "10px",
                    "padding": "5px",
                    "border-radius": "50%",
                    "background-color": "#34679A1a",
                    "border": "1px solid #34679A"
                },
                "regiao": {
                    "color": "#2B7B6F",
                    "font-size": "10px",
                    "padding": "5px",
                    "border-radius": "50%",
                    "background-color": "#2B7B6F1a",
                    "border": "1px solid #2B7B6F"
                },
                "municipio": {
                    "color": "#F7941C",
                    "font-size": "10px",
                    "padding": "5px",
                    "border-radius": "50%",
                    "background-color": "#F7941C1a",
                    "border": "1px solid #F7941C"
                }
            }

            return style_by_type[tipo]
    
    update_button_style_template("indicator-icon-tooth")
    update_button_style_template("indicator-icon-house")
    update_button_style_template("indicator-icon-user-doctor")
    update_button_style_template("indicator-icon-hand-point-right")