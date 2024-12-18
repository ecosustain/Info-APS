"""Módulo para callbacks da população."""

from api.api_requests import get_collection
from callbacks.utils.utils import get_type
from dash import Input, Output


def callback(app):
    """Função para registrar os callbacks da população"""

    @app.callback(
        [
            Output("store-populacao-api", "data"),
            Output("nivel-geo", "data"),
        ],
        [
            Input("dummy-div", "children"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def fetch_population(dummy, estado, regiao, municipio):
        """Função para buscar a populacao do local selecionado"""
        populacao_api = get_collection(
            estado, regiao, municipio, "População", "Cadastros"
        )
        for ano, meses in populacao_api.items():
            media = sum(meses.values()) / len(meses)
            populacao_api[ano] = round(media)

        nivel = get_type(estado, regiao, municipio)
        return populacao_api, nivel
