import dash
from dash import Input, Output, State
from dash import callback_context as ctx

from constants import time_division

def callback(app):
    @app.callback(
        [
            Output(f"btn-{division}", "style")
            for division in time_division.graphic_division
        ],
        [
            Input(f"btn-{division}", "n_clicks")
            for division in time_division.graphic_division
        ],
    )
    def update_button_styles_division(*n_clicks):
        ctx = dash.callback_context

        # Identificar o ano selecionado
        selecionado = time_division.graphic_division[
            0
        ]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn" in prop_id:
                selecionado = prop_id.split(".")[0].split("-")[
                    -1
                ]  # Extrai o ano do ID do botão

        # Atualizar o estilo dos botões com base no ano selecionado
        estilos = []
        for division in time_division.graphic_division:
            if division == selecionado:
                estilo = {
                    "background-color": "#000000",  # Fundo preto
                    "border-color": "#343A40",  # Cor da borda
                    "border": "1px solid #343A40",
                    "color": "#fff",  # Cor do texto
                }
            else:
                estilo = {
                    "background-color": "#FFFFFF",  # Fundo cinza claro
                    "border-color": "#343A40",  # Cor da borda
                    "border": "1px solid #343A40",
                    "color": "#343A40",  # Cor do texto
                }
            estilos.append(estilo)
        return estilos


    @app.callback(
        [
            Output("year-content", "style"),
            Output("quarter-content", "style"),
        ],
        [
            *[
                Input("year-content", "id"),
                Input("quarter-content", "id"),
            ],
            *[
                Input(f"btn-{division}", "n_clicks")
                for division in time_division.graphic_division
            ],
        ],
        [
            *[
                State(f"btn-{division}", "n_clicks")
                for division in time_division.graphic_division
            ],
        ],
    )
    def filter_graphic(*args):
        selecionado = time_division.graphic_division[
            0
        ]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn" in prop_id:
                selecionado = prop_id.split(".")[0].split("-")[-1]

        ids = args[:2]

        dict_division = {"Ano": "year", "Trimestre": "quarter"}

        estilos = []
        for id_graphic in ids:
            if id_graphic.find(dict_division[selecionado]) != -1:
                estilo = {"display": "flex"}
            else:
                estilo = {"display": "none"}
            estilos.append(estilo)
        return estilos