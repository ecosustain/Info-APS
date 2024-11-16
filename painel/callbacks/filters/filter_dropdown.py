"""Módulo para callbacks dos filtros do painel"""

import dash
from api.api_requests import get_municipios
from callbacks.utils.utils import (
    get_municipios_regiao,
    get_regiao_municipio,
    get_regioes,
)
from dash import Input, Output
from dash import callback_context as ctx


def callback(app):
    """Função para registrar os callbacks dos filtros do painel"""

    @app.callback(
        Output("dropdown-regiao", "options"),
        Output("loading-graphics", "display", allow_duplicate=True),
        Input("dropdown-estado", "value"),
        allow_duplicate=True,
        prevent_initial_call=True,
    )
    def update_dropdown_regiao(estado):
        """Função para atualizar as opções do dropdown de regiões"""
        # Função para atualizar as opções do dropdown de municipios
        if estado is None:
            raise dash.exceptions.PreventUpdate
        # Filtrar as municipios do estado selecionado
        regioes = get_regioes(estado)
        # Transformar em um formato aceito pelo dropdown a partir de um dicionário
        options = [
            {"label": regiao, "value": regiao} for regiao in regioes.values()
        ]

        return options, "show"

    @app.callback(
        Output("dropdown-municipio", "options"),
        Output("loading-graphics", "display", allow_duplicate=True),
        [
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
        ],
        allow_duplicate=True,
        prevent_initial_call=True,
    )
    def update_dropdown_municipios(estado, regiao):
        # Função para atualizar as opções do dropdown de municipios
        if estado is None:
            raise dash.exceptions.PreventUpdate
        municipios = get_municipios(estado)
        options = [municipio["cidade"].upper() for municipio in municipios]
        if regiao is not None:
            municipios_regiao = get_municipios_regiao(regiao)
            options = [
                {"label": municipio, "value": municipio}
                for municipio in municipios_regiao.values()
            ]
        return options, "show"

    # Callback para atualizar os dropdowns com base na seleção no mapa
    @app.callback(
        Output("dropdown-estado", "value"),
        Output("dropdown-regiao", "value"),
        Output("dropdown-municipio", "value"),
        Output("loading-graphics", "display", allow_duplicate=True),
        [
            Input("mapa", "clickData"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
        allow_duplicate=True,
        prevent_initial_call=True,
    )
    def update_dropdowns(click_data, estado, regiao, municipio):
        """Função para atualizar os dropdowns com base na seleção no mapa"""
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "dropdown-estado":
            if estado is None:
                return None, None, None, "show"
        if input_id == "dropdown-regiao":
            if regiao is None:
                return estado, None, None, "show"
        if input_id == "dropdown-municipio":
            if municipio is None:
                return estado, regiao, None, "show"
            if municipio is not None and regiao is None:
                regiao = get_regiao_municipio(estado, municipio)
                return estado, regiao, municipio, "show"

        if click_data is None:
            raise dash.exceptions.PreventUpdate

        location = click_data["points"][0]["hovertext"]

        if estado is None and len(location) == 2:
            return location, None, None, "show"
        elif estado is not None and regiao is None:
            return estado, location.upper(), None, "show"
        elif estado is not None and municipio is None:
            return estado, regiao, location.upper(), "show"
        else:
            print("Erro no callback de atualização dos dropdowns")
