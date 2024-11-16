"""Módulo para callbacks do gráfico de mapa"""

from callbacks.map_chart.plotting import (
    get_mapa_brasil,
    get_mapa_estado,
    get_mapa_municipio,
    get_mapa_regiao,
)
from dash import Input, Output


def callback(app):
    """Função para registrar os callbacks do gráfico de mapa"""

    @app.callback(
        Output("mapa", "figure"),
        [
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
            Input("dummy-div", "children"),
        ],
    )
    def update_mapa(estado, regiao, municipio, dummy):
        """Função para atualizar o mapa de acordo com o estado, região ou município selecionado"""
        if municipio:
            return get_mapa_municipio(estado, municipio)
        elif regiao:
            return get_mapa_regiao(estado, regiao)
        elif estado:
            return get_mapa_estado(estado)
        else:
            return get_mapa_brasil()
