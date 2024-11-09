import dash
from callbacks.api_requests import get_atendimentos_individuais_problema
from callbacks.chart_plotting import get_chart_by_quarter, get_chart_by_year 
from callbacks.data_processing import get_df_from_json
from callbacks.utils import get_type
from dash import Input, Output


def register_callbacks_programaticos(app):
    # Callback para fazer a requisição à API e armazenar os dados no dcc.Store
    @app.callback(
        [
            Output("store-data-hipertensao", "data"),
            Output("store-data-diabetes", "data"),
            Output("store-data-saude-sexual", "data"),
            Output("store-data-saude-mental", "data"),
            Output("store-data-puericultura", "data"),
        ],
        [
            Input("dummy-div", "children"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def fetch_programatico_data(dummy, estado, regiao, municipio):
        """Função para fazer a requisição à API e armazenar os dados no Store"""
        data_hipertensao = get_atendimentos_individuais_problema(estado, regiao, municipio, "Hipertensão arterial")
        data_diabetes = get_atendimentos_individuais_problema(estado, regiao, municipio, "Diabetes")
        data_saude_sexual = get_atendimentos_individuais_problema(estado, regiao, municipio, "Saúde sexual e reprodutiva")
        data_saude_mental = get_atendimentos_individuais_problema(estado, regiao, municipio, "Saúde mental")
        data_puericultura = get_atendimentos_individuais_problema(estado, regiao, municipio, "Puericultura")
        #Gravidas
        
        return (
            data_hipertensao,
            data_diabetes,
            data_saude_sexual,
            data_saude_mental,
            data_puericultura,
        )

    @app.callback(
        [
            Output("chart_hipertensao_by_year", "figure"),
            Output("chart_hipertensao_by_quarter", "figure"),
        ],
        [
            Input("store-data-hipertensao", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_hipertensao_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Hipertensão Arterial"
        
        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_diabetes_by_year", "figure"),
            Output("chart_diabetes_by_quarter", "figure"),
        ],
        [
            Input("store-data-diabetes", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_diabetes_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Diabetes"
        
        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_saude_sexual_by_year", "figure"),
            Output("chart_saude_sexual_by_quarter", "figure"),
        ],
        [
            Input("store-data-saude-sexual", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_saude_sexual_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Saúde Sexual"
        
        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_saude_mental_by_year", "figure"),
            Output("chart_saude_mental_by_quarter", "figure"),
        ],
        [
            Input("store-data-saude-mental", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_saude_mental_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Saúde Mental"
        
        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_puericultura_by_year", "figure"),
            Output("chart_puericultura_by_quarter", "figure"),
        ],
        [
            Input("store-data-puericultura", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_puericultura_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Puericultura"
        
        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)
    