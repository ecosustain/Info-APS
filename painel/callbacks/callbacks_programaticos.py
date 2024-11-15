import dash
from api.api_requests import anos, get_atendimentos_individuais_problema
from callbacks.utils.chart_plotting import (
    get_chart_by_quarter,
    get_chart_by_year,
    get_chart_percentage_by_quarter,
    get_chart_percentage_by_year,
)
from callbacks.utils.data_processing import (
    get_df_from_json,
    get_df_gravidez,
    get_gravidez_json,
)
from callbacks.utils.utils import get_type, get_values, store_nivel
from dash import Input, Output, State

# Dicionários para armazenar os históricos dos atendimentos
hist_hipertensao = {}
hist_diabetes = {}
hist_saude_sexual = {}
hist_saude_mental = {}
hist_puericultura = {}
hist_gravidez = {}

data_inputs = [
    Input("dummy-div", "children"),
    Input("dropdown-estado", "value"),
    Input("dropdown-regiao", "value"),
    Input("dropdown-municipio", "value"),
    Input("url", "pathname"),
]
big_numbers_inputs = [
    Input("store-populacao-api", "data"),
    Input("nivel-geo", "data"),
    *[Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
]
big_numbers_states = [
    State("store-data", "data"),
    *[State(f"btn-ano-{ano}", "n_clicks") for ano in anos],
]


def gera_big_numbers(tipo, json, populacao, nivel_geo, ano):
    """Função para gerar os números grandes dos indicadores programáticos"""

    if tipo == "gravidez":
        df = get_df_gravidez(json[0], json[1])
        total = df[df["ano"] == ano]["valor"].sum()
        df_filtered = df[df["ano"] == ano]
        total = (
            df_filtered["valor"].sum() / df_filtered["valor_2"].sum()
            if df_filtered["valor_2"].sum() != 0
            else 0
        )
        total = round(total * 100)
        global hist_gravidez
        hist_gravidez = store_nivel(hist_gravidez, df, None, nivel_geo, anos)
        values = get_values(hist_gravidez, ano, nivel_geo, "mean")
        return values[0], values[1], total

    df = get_df_from_json(json)
    if populacao is not None:
        total = df[df["ano"] == ano]["valor"].sum()
        total = round(total / populacao[str(ano)] * 1000)
    else:
        total = round(df[df["ano"] == ano]["valor"].mean(), 2)

    if tipo == "hipertensao":
        global hist_hipertensao
        hist_hipertensao = store_nivel(
            hist_hipertensao, df, populacao, nivel_geo, anos
        )
        values = get_values(hist_hipertensao, ano, nivel_geo)
    elif tipo == "diabetes":
        global hist_diabetes
        hist_diabetes = store_nivel(
            hist_diabetes, df, populacao, nivel_geo, anos
        )
        values = get_values(hist_diabetes, ano, nivel_geo)
    elif tipo == "saude_sexual":
        global hist_saude_sexual
        hist_saude_sexual = store_nivel(
            hist_saude_sexual, df, populacao, nivel_geo, anos
        )
        values = get_values(hist_saude_sexual, ano, nivel_geo)
    elif tipo == "saude_mental":
        global hist_saude_mental
        hist_saude_mental = store_nivel(
            hist_saude_mental, df, populacao, nivel_geo, anos
        )
        values = get_values(hist_saude_mental, ano, nivel_geo)
    elif tipo == "puericultura":
        global hist_puericultura
        hist_puericultura = store_nivel(
            hist_puericultura, df, populacao, nivel_geo, anos
        )
        values = get_values(hist_puericultura, ano, nivel_geo)
    else:
        return None, None, None

    return values[0], values[1], total


# Função auxiliar para identificar o ano selecionado
def get_selected_year(ctx):
    ano = anos[0]  # Define o primeiro ano como padrão
    if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
        prop_id = ctx.triggered[0]["prop_id"]
        if "btn-ano" in prop_id:
            ano = int(prop_id.split(".")[0].split("-")[-1])
    return ano


def register_callbacks_programaticos(app):

    # Callback para fazer a requisição à API e armazenar os dados de hipertensão no dcc.Store
    @app.callback(
        Output("store-data-hipertensao", "data"),
        data_inputs,
    )
    def fetch_data_hipertensao(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de hipertensão no Store"""
        if url != "/atendimentos-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Hipertensão arterial"
        )

    @app.callback(
        Output("store-data-diabetes", "data"),
        data_inputs,
    )
    def fetch_data_diabetes(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de diabetes no Store"""
        if url != "/atendimentos-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Diabetes"
        )

    @app.callback(
        Output("store-data-saude-sexual", "data"),
        data_inputs,
    )
    def fetch_data_saude_sexual(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de saúde sexual no Store"""
        if url != "/atendimentos-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Saúde sexual e reprodutiva"
        )

    @app.callback(
        Output("store-data-saude-mental", "data"),
        data_inputs,
    )
    def fetch_data_saude_mental(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de saúde mental no Store"""
        if url != "/atendimentos-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Saúde mental"
        )

    @app.callback(
        Output("store-data-puericultura", "data"),
        data_inputs,
    )
    def fetch_data_puericultura(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de puericultura no Store"""
        if url != "/atendimentos-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Puericultura"
        )

    @app.callback(
        Output("store-data-gravidez-adequado", "data"),
        Output("store-data-gravidez-inadequado", "data"),
        data_inputs,
    )
    def fetch_data_gravidez(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados de gravidez no Store"""
        if url != "/atendimentos-programaticos":
            raise dash.exceptions.PreventUpdate
        return get_gravidez_json(estado, regiao, municipio)

    # Callback para atualizar os números grandes de hipertensão
    @app.callback(
        [
            Output("indicador-hipertensao-brasil", "children"),
            Output("indicador-hipertensao-estado", "children"),
            Output("big-hipertensao", "children"),
        ],
        [Input("store-data-hipertensao", "data")] + big_numbers_inputs,
        big_numbers_states,
    )
    def update_hipertensao_big_numbers(
        hipertensao, populacao, nivel_geo, *args
    ):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "hipertensao", hipertensao, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de diabetes
    @app.callback(
        [
            Output("indicador-diabetes-brasil", "children"),
            Output("indicador-diabetes-estado", "children"),
            Output("big-diabetes", "children"),
        ],
        [Input("store-data-diabetes", "data")] + big_numbers_inputs,
        big_numbers_states,
    )
    def update_diabetes_big_numbers(diabetes, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "diabetes", diabetes, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de saúde sexual
    @app.callback(
        [
            Output("indicador-sexual-brasil", "children"),
            Output("indicador-sexual-estado", "children"),
            Output("big-sexual", "children"),
        ],
        [Input("store-data-saude-sexual", "data")] + big_numbers_inputs,
        big_numbers_states,
    )
    def update_sexual_big_numbers(saude_sexual, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "saude_sexual", saude_sexual, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de saúde mental
    @app.callback(
        [
            Output("indicador-mental-brasil", "children"),
            Output("indicador-mental-estado", "children"),
            Output("big-mental", "children"),
        ],
        [Input("store-data-saude-mental", "data")] + big_numbers_inputs,
        big_numbers_states,
    )
    def update_mental_big_numbers(saude_mental, populacao, nivel_geo, *args):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "saude_mental", saude_mental, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de puericultura
    @app.callback(
        [
            Output("indicador-puericultura-brasil", "children"),
            Output("indicador-puericultura-estado", "children"),
            Output("big-puericultura", "children"),
        ],
        [Input("store-data-puericultura", "data")] + big_numbers_inputs,
        big_numbers_states,
    )
    def update_puericultura_big_numbers(
        puericultura, populacao, nivel_geo, *args
    ):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "puericultura", puericultura, populacao, nivel_geo, ano
        )

    # Callback para atualizar os números grandes de gravidez
    @app.callback(
        [
            Output("indicador-gravidas-brasil", "children"),
            Output("indicador-gravidas-estado", "children"),
            Output("big-gravidas", "children"),
        ],
        [
            Input("store-data-gravidez-adequado", "data"),
            Input("store-data-gravidez-inadequado", "data"),
        ]
        + big_numbers_inputs,
        big_numbers_states,
    )
    def update_gravidez_big_numbers(
        gravidez_adequado, gravidez_inadequado, populacao, nivel_geo, *args
    ):
        ano = get_selected_year(dash.callback_context)
        return gera_big_numbers(
            "gravidez",
            [gravidez_adequado, gravidez_inadequado],
            None,
            nivel_geo,
            ano,
        )

    @app.callback(
        [
            Output("chart_hipertensao_by_year", "figure"),
            Output("chart_hipertensao_by_quarter", "figure"),
        ],
        [
            Input("store-data-hipertensao", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_hipertensao_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Hipertensão Arterial"

        df = get_df_from_json(data, populacao)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_diabetes_by_year", "figure"),
            Output("chart_diabetes_by_quarter", "figure"),
        ],
        [
            Input("store-data-diabetes", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_diabetes_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Diabetes"

        df = get_df_from_json(data, populacao)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_saude_sexual_by_year", "figure"),
            Output("chart_saude_sexual_by_quarter", "figure"),
        ],
        [
            Input("store-data-saude-sexual", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_saude_sexual_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Saúde Sexual"

        df = get_df_from_json(data, populacao)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_saude_mental_by_year", "figure"),
            Output("chart_saude_mental_by_quarter", "figure"),
        ],
        [
            Input("store-data-saude-mental", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_saude_mental_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Saúde Mental"

        df = get_df_from_json(data, populacao)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_puericultura_by_year", "figure"),
            Output("chart_puericultura_by_quarter", "figure"),
        ],
        [
            Input("store-data-puericultura", "data"),
            Input("store-populacao-api", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_puericultura_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Puericultura"

        df = get_df_from_json(data, populacao)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)

    @app.callback(
        [
            Output("chart_gravidez_by_year", "figure"),
            Output("chart_gravidez_by_quarter", "figure"),
        ],
        [
            Input("store-data-gravidez-adequado", "data"),
            Input("store-data-gravidez-inadequado", "data"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_gravidez_charts(
        data_adequado, data_inadequado, estado, regiao, municipio
    ):
        if data_adequado is None:
            raise dash.exceptions.PreventUpdate
        titulo = "% de Atendimentos Adequados de Gravidez"
        df = get_df_gravidez(data_adequado, data_inadequado)
        nivel = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_percentage_by_year(df, titulo, nivel)
        chart_by_quarter = get_chart_percentage_by_quarter(df, titulo, nivel)

        return (chart_by_year, chart_by_quarter)
