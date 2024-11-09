import dash
from callbacks.api_requests import get_atendimentos_individuais_problema
from callbacks.chart_plotting import get_chart_by_quarter, get_chart_by_year 
from callbacks.data_processing import get_df_from_json
from callbacks.utils import get_type
from dash import Input, Output
import pandas as pd


def register_callbacks_nao_programaticos(app):
    qtd_hab = 100000
    # Callback para fazer a requisição à API e armazenar os dados no dcc.Store
    @app.callback(
        [
            Output("store-data-asma", "data"),
            Output("store-data-dpoc", "data"),
            Output("store-data-dengue", "data"),
            Output("store-data-tuberculose", "data"),
            Output("store-data-dst", "data"),
            Output("store-data-hanseniase", "data"),
        ],
        [
            Input("dummy-div", "children"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def fetch_data(dummy, estado, regiao, municipio):
        """Função para fazer a requisição à API e armazenar os dados no Store"""

        data_asma = get_atendimentos_individuais_problema(estado, regiao, municipio, "Asma")
        data_dpoc = get_atendimentos_individuais_problema(estado, regiao, municipio, "DPOC")
        data_dengue = get_atendimentos_individuais_problema(estado, regiao, municipio, "DTransmissíveis - Dengue")
        data_tuberculose = get_atendimentos_individuais_problema(estado, regiao, municipio, "DTransmissíveis - Tuberculose")
        data_dst = get_atendimentos_individuais_problema(estado, regiao, municipio, "Doenças transmissíveis - DST")
        data_hanseniase = get_atendimentos_individuais_problema(estado, regiao, municipio, "DTransmissíveis - Hanseníase")
        #TODO
        # vi. Número de atendimentos individuais por mil habitantes que tiveram como CID/CIAP a palavra Febre
        # vii. Número de atendimentos individuais por mil habitantes que tiveram Febre (CIAP A03)
        # viii. Número de atendimentos individuais por mil habitantes que tiveram Dor de Cabeça (CIAP N01)
        # ix. Número de atendimentos individuais por mil habitantes que tiveram Tosse (CIAP R05) 

        
        return (
            data_asma,
            data_dpoc,
            data_dengue,
            data_tuberculose,
            data_dst,
            data_hanseniase,
        )

    @app.callback(
        [
            Output("chart_asma_dpoc_by_year", "figure"),
            Output("chart_asma_dpoc_by_quarter", "figure"),
        ],
        [
            Input("store-data-asma", "data"),
            Input("store-data-dpoc", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_asma_dpoc_charts(data_asma, data_dpoc, populacao, estado, regiao, municipio):
        if data_asma is None:
            raise dash.exceptions.PreventUpdate
        titulo = "ASMA e DPOC"
        
        df_asma = get_df_from_json(data_asma, populacao, qtd_hab)
        df_dpoc = get_df_from_json(data_dpoc, populacao, qtd_hab)
        df =  pd.merge(df_asma, df_dpoc, on=['ano', 'ano_trimestre', 'trimestre', 'mes'], suffixes=('_1', '_2'))
        df['valor'] = df['valor_1'] + df['valor_2']

        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_dengue_by_year", "figure"),
            Output("chart_dengue_by_quarter", "figure"),
        ],
        [
            Input("store-data-dengue", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_dengue_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Dengue"
        
        df = get_df_from_json(data, populacao, qtd_hab)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_tuberculose_by_year", "figure"),
            Output("chart_tuberculose_by_quarter", "figure"),
        ],
        [
            Input("store-data-tuberculose", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_tuberculose_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Tuberculose"
        
        df = get_df_from_json(data, populacao, qtd_hab)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_dst_by_year", "figure"),
            Output("chart_dst_by_quarter", "figure"),
        ],
        [
            Input("store-data-dst", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_dst_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "DST"
        
        df = get_df_from_json(data, populacao, qtd_hab)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_hanseniase_by_year", "figure"),
            Output("chart_hanseniase_by_quarter", "figure"),
        ],
        [
            Input("store-data-hanseniase", "data"),
            Input("store-populacao", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ]
    )
    def update_hanseniase_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Hanseníase"
        
        df = get_df_from_json(data, populacao, qtd_hab)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter( df, titulo, type)
        
        return (chart_by_year, chart_by_quarter)
    