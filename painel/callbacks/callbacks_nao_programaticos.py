"""Módulo para callbacks dos indicadores não programáticos."""

import dash
from api.api_requests import anos, get_atendimentos_individuais_problema
from callbacks.utils.chart_plotting import get_chart_by_quarter, get_chart_by_year
from callbacks.utils.data_processing import (
    get_asma_dpoc_json,
    get_cids_json_cefaleia,
    get_cids_json_febre,
    get_cids_json_tosse,
    get_df_from_json,
)
from callbacks.utils.utils import get_type, get_values, store_nivel
from dash import Input, Output, State

QTD_HAB = 100000

# Dicionários para armazenar os históricos dos atendimentos
hist_asma_dpoc = {}
hist_dengue = {}
hist_tuberculose = {}
hist_dst = {}
hist_hanseniase = {}
hist_cefaleia = {}
hist_tosse = {}
hist_febres = {}

data_inputs = [
    Input("dummy-div", "children"),
    Input("dropdown-estado", "value"),
    Input("dropdown-regiao", "value"),
    Input("dropdown-municipio", "value"),
    Input("url", "pathname"),
]

common_inputs = [
    Input("store-populacao-api", "data"),
    Input("nivel-geo", "data"),
    *[Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
]
common_states = [
    State("store-data", "data"),
    *[State(f"btn-ano-{ano}", "n_clicks") for ano in anos],
]


# Função auxiliar para identificar o ano selecionado
def get_selected_year(ctx):
    """Retorna o ano atual"""
    ano = anos[0]  # Define o primeiro ano como padrão
    if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
        prop_id = ctx.triggered[0]["prop_id"]
        if "btn-ano" in prop_id:
            ano = int(prop_id.split(".")[0].split("-")[-1])
    return ano


def gera_big_numbers(tipo, json, populacao, nivel_geo, ano):
    """Função para gerar os números grandes dos indicadores programáticos"""
    # Add asma_dpoc
    df = get_df_from_json(json)
    total = df[df["ano"] == ano]["valor"].sum()
    total = round(total / populacao[str(ano)] * QTD_HAB)

    if tipo == "asma_dpoc":
        global hist_asma_dpoc
        hist_asma_dpoc = store_nivel(
            hist_asma_dpoc, df, populacao, nivel_geo, anos, QTD_HAB
        )
        values = get_values(hist_asma_dpoc, ano, nivel_geo)
    elif tipo == "dengue":
        global hist_dengue
        hist_dengue = store_nivel(
            hist_dengue, df, populacao, nivel_geo, anos, QTD_HAB
        )
        values = get_values(hist_dengue, ano, nivel_geo)
    elif tipo == "tuberculose":
        global hist_tuberculose
        hist_tuberculose = store_nivel(
            hist_tuberculose, df, populacao, nivel_geo, anos, QTD_HAB
        )
        values = get_values(hist_tuberculose, ano, nivel_geo)
    elif tipo == "dst":
        global hist_dst
        hist_dst = store_nivel(
            hist_dst, df, populacao, nivel_geo, anos, QTD_HAB
        )
        values = get_values(hist_dst, ano, nivel_geo)
    elif tipo == "hanseniase":
        global hist_hanseniase
        hist_hanseniase = store_nivel(
            hist_hanseniase, df, populacao, nivel_geo, anos, QTD_HAB
        )
        values = get_values(hist_hanseniase, ano, nivel_geo)
    elif tipo == "cefaleia":
        global hist_cefaleia
        hist_cefaleia = store_nivel(
            hist_cefaleia, df, populacao, nivel_geo, anos, QTD_HAB
        )
        values = get_values(hist_cefaleia, ano, nivel_geo)
    elif tipo == "tosse":
        global hist_tosse
        hist_tosse = store_nivel(
            hist_tosse, df, populacao, nivel_geo, anos, QTD_HAB
        )
        values = get_values(hist_tosse, ano, nivel_geo)
    elif tipo == "febres":
        global hist_febres
        hist_febres = store_nivel(
            hist_febres, df, populacao, nivel_geo, anos, QTD_HAB
        )
        values = get_values(hist_febres, ano, nivel_geo)
    else:
        values = [None, None]

    return values[0], values[1], total


def register_callbacks_nao_programaticos(app):
    """Callback para fazer a requisição à API e armazenar os dados de asma e DPOC no dcc.Store"""

    @app.callback(
        Output("store-data-asma-dpoc", "data"),
        data_inputs,
    )
    def fetch_data_asma_dpoc(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de asma e DPOC no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_asma_dpoc_json(estado, regiao, municipio)

    # Callback para fazer a requisição à API e armazenar os dados de dengue no dcc.Store
    @app.callback(
        Output("store-data-dengue", "data"),
        data_inputs,
    )
    def fetch_data_dengue(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de dengue no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "DTransmissíveis - Dengue"
        )

    # Callback para fazer a requisição à API e armazenar os dados de tuberculose no dcc.Store
    @app.callback(
        Output("store-data-tuberculose", "data"),
        data_inputs,
    )
    def fetch_data_tuberculose(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de tuberculose no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "DTransmissíveis - Tuberculose"
        )

    # Callback para fazer a requisição à API e armazenar os dados de DST no dcc.Store
    @app.callback(
        Output("store-data-dst", "data"),
        data_inputs,
    )
    def fetch_data_dst(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de DST no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Doenças transmissíveis - DST"
        )

    # Callback para fazer a requisição à API e armazenar os dados de hanseníase no dcc.Store
    @app.callback(
        Output("store-data-hanseniase", "data"),
        data_inputs,
    )
    def fetch_data_hanseniase(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de hanseníase no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "DTransmissíveis - Hanseníase"
        )

    # Callback para fazer a requisição à API e armazenar os dados de cefaleia no dcc.Store
    @app.callback(
        Output("store-data-cefaleia", "data"),
        data_inputs,
    )
    def fetch_data_cefaleia(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de cefaleia no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        data_cefaleia = get_cids_json_cefaleia(estado, regiao, municipio)
        return data_cefaleia

    # Callback para fazer a requisição à API e armazenar os dados de tosse no dcc.Store
    @app.callback(
        Output("store-data-tosse", "data"),
        data_inputs,
    )
    def fetch_data_tosse(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de tosse no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        data_tosse = get_cids_json_tosse(estado, regiao, municipio)
        return data_tosse

    # Callback para fazer a requisição à API e armazenar os dados de febres no dcc.Store
    @app.callback(
        Output("store-data-febres", "data"),
        data_inputs,
    )
    def fetch_data_febres(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de febres no Store"""
        if url != "/atendimentos-nao-programaticos":
            raise dash.exceptions.PreventUpdate
        data_febres = get_cids_json_febre(estado, regiao, municipio)
        return data_febres

    # Callback para atualizar os números grandes de asma e DPOC
    @app.callback(
        [
            Output("indicador-asma-dpoc-brasil", "children"),
            Output("indicador-asma-dpoc-estado", "children"),
            Output("big-asma-dpoc", "children"),
        ],
        [Input("store-data-asma-dpoc", "data")] + common_inputs,
        common_states,
    )
    def update_asma_dpoc_big_numbers(asma_dpoc, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "asma_dpoc", asma_dpoc, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de dengue
    @app.callback(
        [
            Output("indicador-dengue-brasil", "children"),
            Output("indicador-dengue-estado", "children"),
            Output("big-dengue", "children"),
        ],
        [Input("store-data-dengue", "data")] + common_inputs,
        common_states,
    )
    def update_dengue_big_numbers(dengue, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers("dengue", dengue, populacao, nivel_geo, ano)

    # Callback para atualizar os números grandes de tuberculose
    @app.callback(
        [
            Output("indicador-tuberculose-brasil", "children"),
            Output("indicador-tuberculose-estado", "children"),
            Output("big-tuberculose", "children"),
        ],
        [Input("store-data-tuberculose", "data")] + common_inputs,
        common_states,
    )
    def update_tuberculose_big_numbers(
        tuberculose, populacao, nivel_geo, *args
    ):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "tuberculose", tuberculose, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de DST
    @app.callback(
        [
            Output("indicador-dst-brasil", "children"),
            Output("indicador-dst-estado", "children"),
            Output("big-dst", "children"),
        ],
        [Input("store-data-dst", "data")] + common_inputs,
        common_states,
    )
    def update_dst_big_numbers(dst, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers("dst", dst, populacao, nivel_geo, ano)

    # Callback para atualizar os números grandes de hanseníase
    @app.callback(
        [
            Output("indicador-hanseniase-brasil", "children"),
            Output("indicador-hanseniase-estado", "children"),
            Output("big-hanseniase", "children"),
        ],
        [Input("store-data-hanseniase", "data")] + common_inputs,
        common_states,
    )
    def update_hanseniase_big_numbers(hanseniase, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "hanseniase", hanseniase, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de cefaleia
    @app.callback(
        [
            Output("indicador-cefaleia-brasil", "children"),
            Output("indicador-cefaleia-estado", "children"),
            Output("big-cefaleia", "children"),
        ],
        [Input("store-data-cefaleia", "data")] + common_inputs,
        common_states,
    )
    def update_cefaleia_big_numbers(cefaleia, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "cefaleia", cefaleia, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de tosse
    @app.callback(
        [
            Output("indicador-tosse-brasil", "children"),
            Output("indicador-tosse-estado", "children"),
            Output("big-tosse", "children"),
        ],
        [Input("store-data-tosse", "data")] + common_inputs,
        common_states,
    )
    def update_tosse_big_numbers(tosse, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers("tosse", tosse, populacao, nivel_geo, ano)

    # Callback para atualizar os números grandes de febres
    @app.callback(
        [
            Output("indicador-febres-brasil", "children"),
            Output("indicador-febres-estado", "children"),
            Output("big-febres", "children"),
        ],
        [Input("store-data-febres", "data")] + common_inputs,
        common_states,
    )
    def update_febres_big_numbers(febres, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers("febres", febres, populacao, nivel_geo, ano)

    @app.callback(
        [
            Output("chart_asma_dpoc_by_year", "figure"),
            Output("chart_asma_dpoc_by_quarter", "figure"),
        ],
        [
            Input("store-data-asma-dpoc", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_asma_dpoc_charts(
        data_asma, populacao, estado, regiao, municipio
    ):
        if data_asma is None:
            raise dash.exceptions.PreventUpdate
        titulo = "ASMA e DPOC"
        df = get_df_from_json(data_asma, populacao, QTD_HAB)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_dengue_by_year", "figure"),
            Output("chart_dengue_by_quarter", "figure"),
        ],
        [
            Input("store-data-dengue", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_dengue_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Dengue"

        df = get_df_from_json(data, populacao, QTD_HAB)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_tuberculose_by_year", "figure"),
            Output("chart_tuberculose_by_quarter", "figure"),
        ],
        [
            Input("store-data-tuberculose", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_tuberculose_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Tuberculose"

        df = get_df_from_json(data, populacao, QTD_HAB)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_dst_by_year", "figure"),
            Output("chart_dst_by_quarter", "figure"),
        ],
        [
            Input("store-data-dst", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_dst_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "DST"

        df = get_df_from_json(data, populacao, QTD_HAB)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_hanseniase_by_year", "figure"),
            Output("chart_hanseniase_by_quarter", "figure"),
        ],
        [
            Input("store-data-hanseniase", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_hanseniase_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Hanseníase"

        df = get_df_from_json(data, populacao, QTD_HAB)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_cefaleia_by_year", "figure"),
            Output("chart_cefaleia_by_quarter", "figure"),
        ],
        [
            Input("store-data-cefaleia", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_cefaleia_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Cefaleia"

        df = get_df_from_json(data, populacao, QTD_HAB)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_tosse_by_year", "figure"),
            Output("chart_tosse_by_quarter", "figure"),
        ],
        [
            Input("store-data-tosse", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_tosse_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Tosse"

        df = get_df_from_json(data, populacao, QTD_HAB)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_febres_by_year", "figure"),
            Output("chart_febres_by_quarter", "figure"),
        ],
        [
            Input("store-data-febres", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_febres_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Febres"

        df = get_df_from_json(data, populacao, QTD_HAB)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)
