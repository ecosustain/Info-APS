import dash
from dash import Input, Output

from api.api_requests import (
    anos,
    get_atendimentos,
    get_atendimentos_odontologicos,
    get_encaminhamentos,
    get_visitas_domiciliar,
)
from callbacks.utils.chart_plotting import (
    get_chart_by_year,
    get_chart_by_year_profissionais,
    get_chart_forecast_by_quarter,
    get_chart_percentage_by_year,
)
from callbacks.utils.data_processing import (
    get_df_atendimentos,
    get_df_encaminhamentos,
)
from callbacks.utils.utils import (
    get_type,
)

def callback(app):
    @app.callback(
        [
            Output("chart_by_year", "figure", allow_duplicate=True),
            Output("chart_by_year_profissionais", "figure", allow_duplicate=True),
            Output("chart_by_quarter", "figure", allow_duplicate=True),
        ],
        Input("store-data", "data"),
        Input("store-populacao", "data"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
        allow_duplicate=True,
        prevent_initial_call=True
    )
    def update_charts(data, populacao, estado, regiao, municipio):
        df_atendimentos = get_df_atendimentos(data, populacao)

        nivel = get_type(estado, regiao, municipio)

        # Gerar os gráficos
        chart_by_year = get_chart_by_year(
            df_atendimentos, "Atendimentos por mil habitantes", nivel
        )
        chart_by_year_profissionais = get_chart_by_year_profissionais(
            df_atendimentos, "Atendimentos", nivel
        )
        chart_by_quarter = get_chart_forecast_by_quarter(
            df_atendimentos, "Atendimentos por mil habitantes", nivel
        )

        return (
            chart_by_year,
            chart_by_year_profissionais,
            chart_by_quarter,
        )

    data_inputs = [
        Input("dummy-div", "children"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
        Input("url", "pathname"),
    ]

    # Callback para fazer a requisição à API e armazenar os dados no dcc.Store
    @app.callback(
        Output("store-data", "data"),
        data_inputs,
    )
    def fetch_data_atendimentos(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados no Store"""
        if url != "/":
            raise dash.exceptions.PreventUpdate
        data_atendimentos = get_atendimentos(estado, regiao, municipio)
        return data_atendimentos


    # Callback para fazer a requisição à API e armazenar os dados de visitas domiciliares no dcc.Store
    @app.callback(
        Output("store-data-visita", "data"),
        data_inputs,
    )
    def fetch_data_visita(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de visitas domiciliares no Store"""
        if url != "/":
            raise dash.exceptions.PreventUpdate
        return get_visitas_domiciliar(estado, regiao, municipio)

    # Callback para fazer a requisição à API e armazenar os dados de atendimentos odontológicos no dcc.Store
    @app.callback(
        Output("store-data-odonto", "data"),
        data_inputs,
    )
    def fetch_data_odonto(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de atendimentos odontológicos no Store"""
        if url != "/":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_odontologicos(estado, regiao, municipio)

    # Callback para fazer a requisição à API e armazenar os dados de encaminhamentos no dcc.Store
    @app.callback(
        Output("store-data-enc", "data"),
        data_inputs,
    )
    def fetch_data_enc(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de encaminhamentos no Store"""
        if url != "/":
            raise dash.exceptions.PreventUpdate
        return get_encaminhamentos(estado, regiao, municipio)

    @app.callback(
        Output("chart_encaminhamentos", "figure"),
        [
            Input("store-data-enc", "data"),
            Input("store-data", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_chart_encaminhamentos(
        data, atendimentos, populacao, estado, regiao, municipio
    ):
        if data is None or atendimentos is None:
            raise dash.exceptions.PreventUpdate
        df_encaminhamentos = get_df_encaminhamentos(
            data, atendimentos, populacao
        )
        tipo = get_type(estado, regiao, municipio)
        # Gerar o gráfico
        chart_encaminhamentos = get_chart_percentage_by_year(
            df_encaminhamentos,
            "% Encaminhamentos registrados",
            tipo,
        )

        return chart_encaminhamentos