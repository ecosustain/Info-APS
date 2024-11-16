"""Modulo para atualizar os botões de divisão de tempo."""

import dash
from callbacks.utils.utils import get_type
from constants import time_division
from dash import Input, Output, State
from dash import callback_context as ctx


def callback(app):
    """Função para registrar os callbacks dos botões de divisão de tempo"""

    @app.callback(
        [
            Output(f"btn-{division}", "style")
            for division in time_division.graphic_division
        ],
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
        [
            Input(f"btn-{division}", "n_clicks")
            for division in time_division.graphic_division
        ],
    )
    def update_button_styles_division(estado, regiao, municipio, *n_clicks):
        """Função para atualizar o estilo dos botões de divisão"""
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

        tipo = get_type(estado, regiao, municipio)

        style_by_type = {
            "brasil": {"background-color": "#632956"},
            "estado": {"background-color": "#34679A"},
            "regiao": {"background-color": "#2B7B6F"},
            "municipio": {"background-color": "#F7941C"},
        }

        estilos = []
        for division in time_division.graphic_division:
            if division == selecionado:
                estilo = {
                    "background-color": style_by_type[tipo][
                        "background-color"
                    ],  # Fundo preto
                    "border": "none",
                    "color": "#fff",  # Cor do texto
                }
            else:
                estilo = {
                    "background-color": "#FFFFFF",  # Fundo cinza claro
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
                Input("dropdown-estado", "value"),
                Input("dropdown-regiao", "value"),
                Input("dropdown-municipio", "value"),
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
