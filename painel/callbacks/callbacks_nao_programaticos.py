import dash
from dash import Input, Output, State

from callbacks.api_requests import anos, get_atendimentos_individuais_problema
from callbacks.chart_plotting import get_chart_by_quarter, get_chart_by_year 
from callbacks.data_processing import get_df_from_json, get_cids_json
from callbacks.utils import get_type, get_values, store_nivel
import pandas as pd

qtd_hab = 100000
    
# Dicionários para armazenar os históricos dos atendimentos
hist_asma_dpoc = {}
hist_dengue = {}
hist_tuberculose = {}
hist_dst = {}
hist_hanseniase = {}
hist_febre = {}
hist_cefaleia = {}
hist_tosse = {}

def gera_big_numbers(tipo, json, populacao, nivel_geo, ano):
    """Função para gerar os números grandes dos indicadores programáticos"""
    # Add asma_dpoc
    df = get_df_from_json(json)
    total = df[df["ano"] == ano]["valor"].sum()
    total = int(total / populacao * qtd_hab)

    if tipo == "asma_dpoc":
        global hist_asma_dpoc
        hist_asma_dpoc = store_nivel(hist_asma_dpoc, df, populacao, nivel_geo, anos)
        values = get_values(hist_asma_dpoc, ano, nivel_geo)
    elif tipo == "dengue":
        global hist_dengue
        hist_dengue = store_nivel(hist_dengue, df, populacao, nivel_geo, anos)
        values = get_values(hist_dengue, ano, nivel_geo)
    elif tipo == "tuberculose":
        global hist_tuberculose
        hist_tuberculose = store_nivel(hist_tuberculose, df, populacao, nivel_geo, anos)
        values = get_values(hist_tuberculose, ano, nivel_geo)
    elif tipo == "dst":
        global hist_dst
        hist_dst = store_nivel(hist_dst, df, populacao, nivel_geo, anos)
        values = get_values(hist_dst, ano, nivel_geo)
    elif tipo == "hanseniase":
        global hist_hanseniase
        hist_hanseniase = store_nivel(hist_hanseniase, df, populacao, nivel_geo, anos)
        values = get_values(hist_hanseniase, ano, nivel_geo)
    elif tipo == "febre":
        global hist_febre
        hist_febre = store_nivel(hist_febre, df, populacao, nivel_geo, anos)
        values = get_values(hist_febre, ano, nivel_geo)
    elif tipo == "cefaleia":
        global hist_cefaleia
        hist_cefaleia = store_nivel(hist_cefaleia, df, populacao, nivel_geo, anos)
        values = get_values(hist_cefaleia, ano, nivel_geo)
    elif tipo == "tosse":
        global hist_tosse
        hist_tosse = store_nivel(hist_tosse, df, populacao, nivel_geo, anos)
        values = get_values(hist_tosse, ano, nivel_geo)

    return values[0], values[1], total

def register_callbacks_nao_programaticos(app):
    # Callback para fazer a requisição à API e armazenar os dados no dcc.Store
    @app.callback(
        [
            Output("store-data-asma", "data"),
            Output("store-data-dpoc", "data"),
            Output("store-data-dengue", "data"),
            Output("store-data-tuberculose", "data"),
            Output("store-data-dst", "data"),
            Output("store-data-hanseniase", "data"),
            Output("store-data-febre", "data"),
            Output("store-data-cefaleia", "data"),
            Output("store-data-tosse", "data"),
        ],
        [
            Input("dummy-div", "children"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
            Input("url", "pathname"),
        ],
    )
    def fetch_data(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        data_asma = get_atendimentos_individuais_problema(estado, regiao, municipio, "Asma")
        data_dpoc = get_atendimentos_individuais_problema(estado, regiao, municipio, "DPOC")
        data_dengue = get_atendimentos_individuais_problema(estado, regiao, municipio, "DTransmissíveis - Dengue")
        data_tuberculose = get_atendimentos_individuais_problema(estado, regiao, municipio, "DTransmissíveis - Tuberculose")
        data_dst = get_atendimentos_individuais_problema(estado, regiao, municipio, "Doenças transmissíveis - DST")
        data_hanseniase = get_atendimentos_individuais_problema(estado, regiao, municipio, "DTransmissíveis - Hanseníase")
        data_febre, data_cefaleia, data_tosse = get_cids_json(estado, regiao, municipio)
        #TODO
        # vi. Número de atendimentos individuais por mil habitantes que tiveram como CID/CIAP a palavra Febre
        
        return (
            data_asma,
            data_dpoc,
            data_dengue,
            data_tuberculose,
            data_dst,
            data_hanseniase,
            data_febre,
            data_cefaleia,
            data_tosse,
        )

    @app.callback(
        [
            # Output("indicador-asma_dpoc-brasil", "children"),
            # Output("indicador-asma_dpoc-estado", "children"),
            # Output("big-asma_dpoc", "children"),
            Output("indicador-dengue-brasil", "children"),
            Output("indicador-dengue-estado", "children"),
            Output("big-dengue", "children"),
            Output("indicador-tuberculose-brasil", "children"),
            Output("indicador-tuberculose-estado", "children"),
            Output("big-tuberculose", "children"),
            Output("indicador-dst-brasil", "children"),
            Output("indicador-dst-estado", "children"),
            Output("big-dst", "children"),
            Output("indicador-hanseniase-brasil", "children"),
            Output("indicador-hanseniase-estado", "children"),
            Output("big-hanseniase", "children"),
            Output("indicador-febre-brasil", "children"),
            Output("indicador-febre-estado", "children"),
            Output("big-febre", "children"),
            Output("indicador-cefaleia-brasil", "children"),
            Output("indicador-cefaleia-estado", "children"),
            Output("big-cefaleia", "children"),
            Output("indicador-tosse-brasil", "children"),
            Output("indicador-tosse-estado", "children"),
            Output("big-tosse", "children"),
        ],
        [
            # Input("store-data-asma", "data"),
            # Input("store-data-dpoc", "data"),
            Input("store-data-dengue", "data"),
            Input("store-data-tuberculose", "data"),
            Input("store-data-dst", "data"),
            Input("store-data-hanseniase", "data"),
            Input("store-data-febre", "data"),
            Input("store-data-cefaleia", "data"),
            Input("store-data-tosse", "data"),
            Input("store-populacao", "data"),
            Input("nivel-geo", "data"),
            *[Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
        [
            State("store-data", "data"),
            *[State(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
    )
    def update_programatico_big_numbers(
        # asma,
        # dpoc,
        dengue,
        tuberculose,
        dst,
        hanseniase,
        febre,
        cefaleia,
        tosse,
        populacao,
        nivel_geo,
        *args,
    ):
        """Função para atualizar os números grandes dos indicadores programáticos"""
        ctx = dash.callback_context
        # Identificar o ano selecionado
        ano = anos[0]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-ano" in prop_id:
                ano = int(
                    ctx.triggered[0]["prop_id"].split(".")[0].split("-")[-1]
                )  # Extrai o ano do ID do botão

        # Inicializa a lista para armazenar os números grandes
        big_numbers = []

        # # Add asma_dpoc
        # big_numbers.append(
        #     gera_big_numbers("asma_dpoc", asma_dpoc, populacao, nivel_geo, ano)
        # )
        # Add dengue
        big_numbers.append(
            gera_big_numbers("dengue", dengue, populacao, nivel_geo, ano)
        )
        # Add tuberculose
        big_numbers.append(
            gera_big_numbers("tuberculose", tuberculose, populacao, nivel_geo, ano)
        )
        # Add dst
        big_numbers.append(
            gera_big_numbers("dst", dst, populacao, nivel_geo, ano)
        )
        # Add hanseniase
        big_numbers.append(
            gera_big_numbers("hanseniase", hanseniase, populacao, nivel_geo, ano)
        )
        # Add febre
        big_numbers.append(
            gera_big_numbers("febre", febre, populacao, nivel_geo, ano)
        )
        # Add cefaleia
        big_numbers.append(
            gera_big_numbers("cefaleia", cefaleia, populacao, nivel_geo, ano)
        )
        # Add tosse
        big_numbers.append(
            gera_big_numbers("tosse", tosse, populacao, nivel_geo, ano)
        )

        big_numbers = [item for sublist in big_numbers for item in sublist]

        return big_numbers

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
    