"""Módulo com os callbacks da página Principal"""

import warnings

import dash
from callbacks.api_requests import (
    anos,
    get_atendimentos,
    get_atendimentos_odontologicos,
    get_encaminhamentos,
    get_municipios,
    get_visitas_domiciliar,
    get_collection,
)
from callbacks.chart_plotting import (
    get_chart_by_year,
    get_chart_by_year_profissionais,
    get_chart_forecast_by_quarter,
    get_chart_percentage_by_year,
)
from callbacks.data_processing import (
    get_big_numbers_atendimentos,
    get_df_atendimentos,
    get_df_encaminhamentos,
    get_df_from_json,
)
from callbacks.map_plotting import (
    get_mapa_brasil,
    get_mapa_estado,
    get_mapa_municipio,
    get_mapa_regiao,
)
from callbacks.utils import (
    formatar_numero,
    get_municipios_regiao,
    get_population,
    get_regiao_municipio,
    get_regioes,
    get_type,
    get_values,
    store_nivel,
)
from constants import time_division
from dash import Input, Output, State
from dash import callback_context as ctx
from statsmodels.tools.sm_exceptions import ConvergenceWarning

# from paginas import tela_inicial, tela_visitas, tela_odonto
hist_atend = {}
hist_odont = {}
hist_visita = {}

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Non-invertible starting seasonal moving average",
)
warnings.filterwarnings("ignore", category=ConvergenceWarning)


def register_callbacks(app):
    """Função para registrar os callbacks do painel principal"""

    @app.callback(
        Output("dropdown-regiao", "options"),
        Input("dropdown-estado", "value"),
    )
    def update_dropdown_regiao(estado):
        # Função para atualizar as opções do dropdown de municipios
        if estado is None:
            raise dash.exceptions.PreventUpdate

        # Filtrar as municipios do estado selecionado
        regioes = get_regioes(estado)

        # Transformar em um formato aceito pelo dropdown a partir de um dicionário
        options = [
            {"label": regiao, "value": regiao} for regiao in regioes.values()
        ]

        return options

    @app.callback(
        Output("dropdown-municipio", "options"),
        [
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
        ],
    )
    def update_dropdown_municipios(estado, regiao):
        # Função para atualizar as opções do dropdown de municipios
        if estado is None:
            raise dash.exceptions.PreventUpdate
        municipios = get_municipios(estado)
        options = [municipio["cidade"].upper() for municipio in municipios]
        if regiao is not None:
            municipios_regiao = get_municipios_regiao(regiao)
            options = [
                {"label": municipio, "value": municipio}
                for municipio in municipios_regiao.values()
            ]
        return options

    @app.callback(
        [
            Output("store-populacao", "data"),
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
        populacao = get_population(estado, regiao, municipio)
        populacao_api = get_collection(estado, regiao, municipio, 'População', 'Cadastros')
        nivel = get_type(estado, regiao, municipio)
        return populacao, populacao_api, nivel


# Callback para fazer a requisição à API e armazenar os dados no dcc.Store
    @app.callback(
        
        Output("store-data", "data"),
        [
            Input("dummy-div", "children"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
            Input("url", "pathname"),
        ],
    )
    def fetch_data_atendimentos(dummy, estado, regiao, municipio, url):
        """Função para fazer a requisição à API e armazenar os dados no Store"""
        if url != "/":
            raise dash.exceptions.PreventUpdate
        data_atendimentos = get_atendimentos(estado, regiao, municipio)
        return data_atendimentos


    # Callback para fazer a requisição à API e armazenar os dados no dcc.Store
    @app.callback(
        [
            Output("store-data-visita", "data"),
            Output("store-data-odonto", "data"),
            Output("store-data-enc", "data"),
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
        if url != "/":
            raise dash.exceptions.PreventUpdate
        data_visitas_domiciliar = get_visitas_domiciliar(
            estado, regiao, municipio
        )
        data_atendimentos_odontologicos = get_atendimentos_odontologicos(
            estado, regiao, municipio
        )
        data_encaminhamentos = get_encaminhamentos(estado, regiao, municipio)

        return (
            data_visitas_domiciliar,
            data_atendimentos_odontologicos,
            data_encaminhamentos,
        )

    @app.callback(
        [
            Output("indicador-atend-brasil", "children"),
            Output("indicador-atend-estado", "children"),
            Output("total-atendimentos", "children"),
            Output("normalizado-atendimentos", "children"),
            Output("big-medicos", "children"),
        ],
        [
            Input("store-data", "data"),
            Input("store-populacao-api", "data"),
            Input("nivel-geo", "data"),
            *[Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
        [
            State("store-data", "data"),
            *[State(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
    )
    def update_big_numbers_atend(data, populacao, nivel, *args):
        """Função para atualizar os big numbers com base nos dados armazenados"""
        ctx = dash.callback_context
        # Identificar o ano selecionado
        ano = anos[0]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-ano" in prop_id:
                ano = int(
                    ctx.triggered[0]["prop_id"].split(".")[0].split("-")[-1]
                )  # Extrai o ano do ID do botão

        if data is None:
            raise dash.exceptions.PreventUpdate

        populacao = round(sum(populacao[str(ano)].values()) / len(populacao[str(ano)]))
        df = get_df_atendimentos(data)
        big_numbers = get_big_numbers_atendimentos(df, ano)
        global hist_atend
        hist_atend = store_nivel(hist_atend, df, populacao, nivel, anos)
        # Normalizar os valores pelo total da população
        total_populacao = populacao / 1000
        total_atendimentos = big_numbers[0]
        total_atendimentos = formatar_numero(total_atendimentos)

        # Dividir cada big number por 1000 para facilitar a leitura
        big_numbers = [int(num / total_populacao) for num in big_numbers]
        # Inserir o total de atendimentos no primeiro lugar
        big_numbers.insert(0, total_atendimentos)

        values = get_values(hist_atend, ano, nivel)

        big_numbers.insert(0, values[1])
        big_numbers.insert(0, values[0])

        return big_numbers



    @app.callback(
        [
            Output("indicador-visita-brasil", "children"),
            Output("indicador-visita-estado", "children"),
            Output("indicador-odont-brasil", "children"),
            Output("indicador-odont-estado", "children"),
            Output("big-encaminhamentos", "children"),
            Output("big-visitas", "children"),
            Output("big-odontologicos", "children"),
        ],
        [
            Input("store-data", "data"),
            Input("store-data-enc", "data"),
            Input("store-data-visita", "data"),
            Input("store-data-odonto", "data"),
            Input("store-populacao-api", "data"),
            Input("nivel-geo", "data"),
            *[Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
        [
            State("store-data", "data"),
            *[State(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
    )
    def update_big_numbers(
        data, data_enc, data_visita, data_odonto, populacao, nivel, *args
    ):
        """Função para atualizar os big numbers com base nos dados armazenados"""
        ctx = dash.callback_context
        # Identificar o ano selecionado
        ano = anos[0]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-ano" in prop_id:
                ano = int(
                    ctx.triggered[0]["prop_id"].split(".")[0].split("-")[-1]
                )  # Extrai o ano do ID do botão

        if data is None:
            raise dash.exceptions.PreventUpdate

        populacao = round(sum(populacao[str(ano)].values()) / len(populacao[str(ano)]))

        big_numbers = []

        # Add encaminhamento
        df_enc = get_df_from_json(data_enc)
        total_enc_ano = df_enc[df_enc["ano"] == ano]["valor"].sum()
        big_numbers.append(total_enc_ano)

        # Add visitas domiciliar
        df_visita = get_df_from_json(data_visita)
        total_visita_ano = df_visita[df_visita["ano"] == ano]["valor"].sum()
        big_numbers.append(total_visita_ano)
        global hist_visita
        hist_visita = store_nivel(
            hist_visita, df_visita, populacao, nivel, anos
        )

        # Add atendimentos odontologicos
        df_odonto = get_df_from_json(data_odonto)
        total_odonto_ano = df_odonto[df_odonto["ano"] == ano]["valor"].sum()
        big_numbers.append(total_odonto_ano)
        global hist_odont
        hist_odont = store_nivel(hist_odont, df_odonto, populacao, nivel, anos)

        # Normalizar os valores pelo total da população
        total_populacao = populacao / 1000

        # Dividir cada big number por 1000 para facilitar a leitura
        big_numbers = [int(num / total_populacao) for num in big_numbers]

        values = get_values(hist_odont, ano, nivel)

        big_numbers.insert(0, values[1])
        big_numbers.insert(0, values[0])

        values = get_values(hist_visita, ano, nivel)

        big_numbers.insert(0, values[1])
        big_numbers.insert(0, values[0])

        return big_numbers

    # Callback para atualizar os gráficos de atendimentos com base nos dados armazenados
    @app.callback(
        [
            Output("chart_by_year", "figure"),
            Output("chart_by_year_profissionais", "figure"),
            Output("chart_by_quarter", "figure"),
        ],
        Input("store-data", "data"),
        Input("store-populacao", "data"),
        Input("dropdown-estado", "value"),
        Input("dropdown-regiao", "value"),
        Input("dropdown-municipio", "value"),
    )
    def update_charts(data, populacao, estado, regiao, municipio):
        if data is None:
            raise dash.exceptions.PreventUpdate
        df_atendimentos = get_df_atendimentos(data, populacao)

        nivel = get_type(estado, regiao, municipio)

        # Gerar os gráficos
        chart_by_year = get_chart_by_year(
            df_atendimentos, "Atendimentos por mil hab.", nivel
        )
        chart_by_year_profissionais = get_chart_by_year_profissionais(
            df_atendimentos, "Atendimentos por profissionais", nivel
        )
        chart_by_quarter = get_chart_forecast_by_quarter(
            df_atendimentos, "Atendimentos por mil hab.", nivel
        )

        return (
            chart_by_year,
            chart_by_year_profissionais,
            chart_by_quarter,
        )

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

    # Callback para atualizar o mapa com base nos dropdowns
    @app.callback(
        Output("mapa", "figure"),
        [
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
            Input("dummy-div", "children"),
        ],
    )
    def update_mapa(estado, regiao, municipio, dummy):
        if estado is None and municipio is None and regiao is None:
            return get_mapa_brasil()
        elif estado is not None and regiao is None and municipio is None:
            return get_mapa_estado(estado)
        elif estado is not None and regiao is not None and municipio is None:
            return get_mapa_regiao(estado, regiao)
        elif estado is not None and municipio is not None:
            return get_mapa_municipio(estado, municipio)
        return get_mapa_brasil()

    # Callback para atualizar os dropdowns com base na seleção no mapa
    @app.callback(
        Output("dropdown-estado", "value"),
        Output("dropdown-regiao", "value"),
        Output("dropdown-municipio", "value"),
        [
            Input("mapa", "clickData"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
        ],
    )
    def update_dropdowns(clickData, estado, regiao, municipio):
        """Função para atualizar os dropdowns com base na seleção no mapa"""
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "dropdown-estado":
            if estado is None:
                return None, None, None
        if input_id == "dropdown-regiao":
            if regiao is None:
                return estado, None, None
        if input_id == "dropdown-municipio":
            if municipio is None:
                return estado, regiao, None
            if municipio is not None and regiao is None:
                regiao = get_regiao_municipio(estado, municipio)
                return estado, regiao, municipio

        if clickData is None:
            raise dash.exceptions.PreventUpdate

        location = clickData["points"][0]["hovertext"]

        if estado is None and len(location) == 2:
            return location, None, None
        elif estado is not None and regiao is None:
            return estado, location.upper(), None
        elif estado is not None and municipio is None:
            return estado, regiao, location.upper()
        else:
            print("Erro no callback de atualização dos dropdowns")

    @app.callback(
        [Output(f"btn-ano-{ano}", "style") for ano in anos],
        [Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
    )
    def update_button_styles_ano(*n_clicks):
        ctx = dash.callback_context

        # Identificar o ano selecionado
        ano_selecionado = anos[0]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn-ano" in prop_id:
                ano_selecionado = int(
                    prop_id.split(".")[0].split("-")[-1]
                )  # Extrai o ano do ID do botão

        # Atualizar o estilo dos botões com base no ano selecionado
        estilos = []
        for ano in anos:
            if ano == ano_selecionado:
                estilo = {
                    "background-color": "#000000",  # Fundo preto
                    "border-color": "#343A40",  # Cor da borda
                    "border": "1px solid #343A40",
                    "color": "#fff",  # Cor do texto
                }
            else:
                estilo = {
                    "background-color": "#FFFFFF",  # Fundo cinza claro
                    "border-color": "#343A40",  # Cor da borda
                    "border": "1px solid #343A40",
                    "color": "#343A40",  # Cor do texto
                }
            estilos.append(estilo)
        return estilos

    @app.callback(
        [
            Output(f"btn-{division}", "style")
            for division in time_division.graphic_division
        ],
        [
            Input(f"btn-{division}", "n_clicks")
            for division in time_division.graphic_division
        ],
    )
    def update_button_styles_division(*n_clicks):
        ctx = dash.callback_context

        # Identificar o ano selecionado
        selecionado = time_division.graphic_division[
            0
        ]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn" in prop_id:
                selecionado = prop_id.split(".")[0].split("-")[
                    -1
                ]  # Extrai o ano do ID do botão

        # Atualizar o estilo dos botões com base no ano selecionado
        estilos = []
        for division in time_division.graphic_division:
            if division == selecionado:
                estilo = {
                    "background-color": "#000000",  # Fundo preto
                    "border-color": "#343A40",  # Cor da borda
                    "border": "1px solid #343A40",
                    "color": "#fff",  # Cor do texto
                }
            else:
                estilo = {
                    "background-color": "#FFFFFF",  # Fundo cinza claro
                    "border-color": "#343A40",  # Cor da borda
                    "border": "1px solid #343A40",
                    "color": "#343A40",  # Cor do texto
                }
            estilos.append(estilo)
        return estilos

    @app.callback(
        [
            Output("year-content", "style"),
            Output("quarter-content", "style"),
        ],
        [
            *[
                Input("year-content", "id"),
                Input("quarter-content", "id"),
            ],
            *[
                Input(f"btn-{division}", "n_clicks")
                for division in time_division.graphic_division
            ],
        ],
        [
            *[
                State(f"btn-{division}", "n_clicks")
                for division in time_division.graphic_division
            ],
        ],
    )
    def filter_graphic(*args):
        selecionado = time_division.graphic_division[
            0
        ]  # Define o primeiro ano como padrão
        if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
            prop_id = ctx.triggered[0]["prop_id"]
            if "btn" in prop_id:
                selecionado = prop_id.split(".")[0].split("-")[-1]

        ids = args[:2]

        dict_division = {"Ano": "year", "Trimestre": "quarter"}

        estilos = []
        for id_graphic in ids:
            if id_graphic.find(dict_division[selecionado]) != -1:
                estilo = {"display": "block"}
            else:
                estilo = {"display": "none"}
            estilos.append(estilo)
        return estilos
