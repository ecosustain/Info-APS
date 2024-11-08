import dash
from callbacks.chart_plotting import get_chart_by_quarter
from callbacks.data_processing import get_df_from_json
from callbacks.utils import get_type
from dash import Input, Output


def register_callbacks_visita(app):
    @app.callback(
        [
            Output("chart_visitas_by_quarter", "figure"),
        ],
        Input("store-data", "data"),
        Input("store-data-visita", "data"),
        Input("store-populacao", "data"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
    )
    def update_charts(data, data_visita, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        df_visita = get_df_from_json(data_visita, populacao)

        type = get_type(estado, regiao, municipio)

        chart_visitas_by_quarter = get_chart_by_quarter(
            df_visita, "Atendimentos por mil habitantes", type
        )

        return (chart_visitas_by_quarter,)
