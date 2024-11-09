import dash
from dash import Input, Output, State

from callbacks.api_requests import anos, get_atendimentos_individuais_problema
from callbacks.chart_plotting import get_chart_by_quarter, get_chart_by_year
from callbacks.data_processing import get_df_from_json
from callbacks.utils import get_type, get_values, store_nivel

# Dicionários para armazenar os históricos dos atendimentos
hist_hipertensao = {}
hist_diabetes = {}
hist_saude_sexual = {}
hist_saude_mental = {}
hist_puericultura = {}


def gera_big_numbers(tipo, json, populacao, nivel_geo, ano):
    """Função para gerar os números grandes dos indicadores programáticos"""
    # Add hipertensao
    df = get_df_from_json(json)
    total = df[df["ano"] == ano]["valor"].sum()
    total = int(total / populacao * 1000)

    if tipo == "hipertensao":
        global hist_hipertensao
        hist_hipertensao = store_nivel(hist_hipertensao, df, populacao, nivel_geo, anos)
        values = get_values(hist_hipertensao, ano, nivel_geo)
    elif tipo == "diabetes":
        global hist_diabetes
        hist_diabetes = store_nivel(hist_diabetes, df, populacao, nivel_geo, anos)
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

    return values[0], values[1], total


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
            Input("url", "pathname"),
        ],
    )
    def fetch_programatico_data(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados no Store"""
        if url != "/atendimentos-programaticos":
            raise dash.exceptions.PreventUpdate
        data_hipertensao = get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Hipertensão arterial"
        )
        data_diabetes = get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Diabetes"
        )
        data_saude_sexual = get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Saúde sexual e reprodutiva"
        )
        data_saude_mental = get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Saúde mental"
        )
        data_puericultura = get_atendimentos_individuais_problema(
            estado, regiao, municipio, "Puericultura"
        )
        # Gravidas

        return (
            data_hipertensao,
            data_diabetes,
            data_saude_sexual,
            data_saude_mental,
            data_puericultura,
        )

    @app.callback(
        [
            Output("indicador-hipertensao-brasil", "children"),
            Output("indicador-hipertensao-estado", "children"),
            Output("big-hipertensao", "children"),
            Output("indicador-diabetes-brasil", "children"),
            Output("indicador-diabetes-estado", "children"),
            Output("big-diabetes", "children"),
            Output("indicador-sexual-brasil", "children"),
            Output("indicador-sexual-estado", "children"),
            Output("big-sexual", "children"),
            Output("indicador-mental-brasil", "children"),
            Output("indicador-mental-estado", "children"),
            Output("big-mental", "children"),
            Output("indicador-puericultura-brasil", "children"),
            Output("indicador-puericultura-estado", "children"),
            Output("big-puericultura", "children"),
            Output("indicador-gravidas-brasil", "children"),
            Output("indicador-gravidas-estado", "children"),
            Output("big-gravidas", "children"),
        ],
        [
            Input("store-data-hipertensao", "data"),
            Input("store-data-diabetes", "data"),
            Input("store-data-saude-sexual", "data"),
            Input("store-data-saude-mental", "data"),
            Input("store-data-puericultura", "data"),
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
        hipertensao,
        diabetes,
        saude_sexual,
        saude_mental,
        puericultura,
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

        # Add hipertensao
        big_numbers.append(
            gera_big_numbers("hipertensao", hipertensao, populacao, nivel_geo, ano)
        )
        # Add diabetes
        big_numbers.append(
            gera_big_numbers("diabetes", diabetes, populacao, nivel_geo, ano)
        )
        # Add saude_sexual
        big_numbers.append(
            gera_big_numbers("saude_sexual", saude_sexual, populacao, nivel_geo, ano)
        )
        # Add saude_mental
        big_numbers.append(
            gera_big_numbers("saude_mental", saude_mental, populacao, nivel_geo, ano)
        )
        # Add puericultura
        big_numbers.append(
            gera_big_numbers("puericultura", puericultura, populacao, nivel_geo, ano)
        )
        # Gravidas
        big_numbers.append([None, None, None])

        big_numbers = [item for sublist in big_numbers for item in sublist]
        print(big_numbers)

        return big_numbers

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
        ],
    )
    def update_hipertensao_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Hipertensão Arterial"

        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter(df, titulo, type)

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
        ],
    )
    def update_diabetes_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Diabetes"

        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter(df, titulo, type)

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
        ],
    )
    def update_saude_sexual_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Saúde Sexual"

        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter(df, titulo, type)

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
        ],
    )
    def update_saude_mental_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Saúde Mental"

        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter(df, titulo, type)

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
        ],
    )
    def update_puericultura_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        titulo = "Puericultura"

        df = get_df_from_json(data, populacao)
        type = get_type(estado, regiao, municipio)
        chart_by_year = get_chart_by_year(df, titulo, type)
        chart_by_quarter = get_chart_by_quarter(df, titulo, type)

        return (chart_by_year, chart_by_quarter)
