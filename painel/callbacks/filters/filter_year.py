"""Módulo para callbacks dos filtros de anos."""

import dash
from api.api_requests import anos
from callbacks.utils.utils import get_type
from dash import Input, Output


def callback(app):
    """Função para registrar os callbacks dos filtros de anos"""

    @app.callback(
        [Output(f"btn-ano-{ano}", "style") for ano in anos],
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
        [Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
    )
    def update_button_styles_ano(estado, regiao, municipio, *n_clicks):
        """Função para atualizar o estilo dos botões de ano"""
        ctx = dash.callback_context

        # Identificar o ano selecionado
        ano_selecionado = anos[0]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-ano" in prop_id:
                ano_selecionado = int(
                    prop_id.split(".")[0].split("-")[-1]
                )  # Extrai o ano do ID do botão

        tipo = get_type(estado, regiao, municipio)

        style_by_type = {
            "brasil": {"background-color": "#632956"},
            "estado": {"background-color": "#34679A"},
            "regiao": {"background-color": "#2B7B6F"},
            "municipio": {"background-color": "#F7941C"},
        }

        estilos = []
        for ano in anos:
            if ano == ano_selecionado:
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
