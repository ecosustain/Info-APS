"""Modulo com os callbacks para os gráficos de visitas domiciliares."""

import dash
from callbacks.utils.chart_plotting import get_chart_by_quarter, get_chart_by_year
from callbacks.utils.data_processing import get_df_from_json
from callbacks.utils.utils import get_type
from dash import Input, Output


def register_callbacks_visita(app):
    """Função para registrar os callbacks dos atendimentos odontológicos."""

    @app.callback(
        [
            Output("chart_visitas_by_quarter", "figure"),
            Output("chart_visitas_by_year", "figure"),
        ],
        Input("store-data", "data"),
        Input("store-data-visita", "data"),
        Input("store-populacao-api", "data"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
    )
    def update_charts(data, data_visita, populacao, estado, regiao, municipio):
        """Função para atualizar os gráficos de visitas domiciliares."""
        if data is None:
            raise dash.exceptions.PreventUpdate
        df_visita = get_df_from_json(data_visita, populacao)

        nivel = get_type(estado, regiao, municipio)

        chart_visitas_by_quarter = get_chart_by_quarter(
            df_visita, "Visitas Domiciliar por mil hab.", nivel
        )

        chart_visitas_by_year = get_chart_by_year(
            df_visita, "Visitas Domiciliar por mil hab.", nivel
        )

        return (chart_visitas_by_quarter, chart_visitas_by_year)
