import dash
from api.api_requests import anos
from callbacks.utils.data_processing import (
    get_big_numbers_atendimentos,
    get_df_atendimentos,
    get_df_from_json,
    soma_atendimentos
)
from callbacks.utils.utils import formatar_numero, get_values, store_nivel
from dash import Input, Output, State


def get_selected_year(ctx):
    """Retorna o ano atual"""
    ano = anos[0]  # Define o primeiro ano como padrão
    if ctx.triggered and ctx.triggered[0]["prop_id"] != ".":
        prop_id = ctx.triggered[0]["prop_id"]
        if "btn-ano" in prop_id:
            ano = int(prop_id.split(".")[0].split("-")[-1])
    return ano


data_states = [
    State("store-data", "data"),
    *[State(f"btn-ano-{ano}", "n_clicks") for ano in anos],
]

big_numbers_input = [
    Input("store-populacao-api", "data"),
    Input("nivel-geo", "data"),
    *[Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
]

hist_atend = {}
hist_odont = {}
hist_visita = {}


def callback(app):
    @app.callback(
        Output("big-encaminhamentos", "children"),
        [
            Input("store-data-enc", "data"),
            Input("store-data", "data"),
            *[Input(f"btn-ano-{ano}", "n_clicks") for ano in anos],
        ],
        data_states,
    )
    def update_encaminhamentos_big_numbers(data_enc, data_atend, *args):
        ano = get_selected_year(dash.callback_context)

        # Add encaminhamento
        df_enc = get_df_from_json(data_enc)
        total_enc_ano = df_enc[df_enc["ano"] == ano]["valor"].sum()

        total_atend = soma_atendimentos(data_atend)
        df_atendimentos = get_df_from_json(total_atend)
        total_atend_ano = df_atendimentos[df_atendimentos["ano"] == ano]["valor"].sum()

        big_numbers = [round((total_enc_ano / total_atend_ano)*100, 2)]

        return big_numbers

    # Callback para atualizar os números grandes de visitas domiciliares
    @app.callback(
        [
            Output("indicador-visita-brasil", "children"),
            Output("indicador-visita-estado", "children"),
            Output("big-visitas", "children"),
        ],
        [Input("store-data-visita", "data")] + big_numbers_input,
        data_states,
    )
    def update_visita_big_numbers(data_visita, populacao, nivel, *args):
        ano = get_selected_year(dash.callback_context)

        # Add visitas domiciliar
        df_visita = get_df_from_json(data_visita)
        total_visita_ano = df_visita[df_visita["ano"] == ano]["valor"].sum()
        global hist_visita
        hist_visita = store_nivel(
            hist_visita, df_visita, populacao, nivel, anos
        )

        # Normalizar os valores pelo total da população
        total_populacao = populacao[str(ano)] / 1000
        big_numbers = [round(total_visita_ano / total_populacao)]

        values = get_values(hist_visita, ano, nivel)
        big_numbers.insert(0, values[1])
        big_numbers.insert(0, values[0])

        return big_numbers

    # Callback para atualizar os números grandes de atendimentos odontológicos
    @app.callback(
        [
            Output("indicador-odont-brasil", "children"),
            Output("indicador-odont-estado", "children"),
            Output("big-odontologicos", "children"),
        ],
        [Input("store-data-odonto", "data")] + big_numbers_input,
        data_states,
    )
    def update_odont_big_numbers(data_odonto, populacao, nivel, *args):
        ano = get_selected_year(dash.callback_context)

        # Add atendimentos odontologicos
        df_odonto = get_df_from_json(data_odonto)
        total_odonto_ano = df_odonto[df_odonto["ano"] == ano]["valor"].sum()
        global hist_odont
        hist_odont = store_nivel(hist_odont, df_odonto, populacao, nivel, anos)

        # Normalizar os valores pelo total da população
        total_populacao = populacao[str(ano)] / 1000
        big_numbers = [round(total_odonto_ano / total_populacao)]

        values = get_values(hist_odont, ano, nivel)
        big_numbers.insert(0, values[1])
        big_numbers.insert(0, values[0])

        return big_numbers

    @app.callback(
        [
            Output("indicador-atend-brasil", "children"),
            Output("indicador-atend-estado", "children"),
            Output("total-atendimentos", "children"),
            Output("normalizado-atendimentos", "children"),
            Output("big-medicos", "children"),
        ],
        [Input("store-data", "data")] + big_numbers_input,
        data_states,
    )
    def update_big_numbers_atend(data, populacao, nivel, *args):
        """Função para atualizar os big numbers com base nos dados armazenados"""
        if data is None:
            raise dash.exceptions.PreventUpdate
        ano = get_selected_year(dash.callback_context)
        df = get_df_atendimentos(data)
        big_numbers = get_big_numbers_atendimentos(df, ano)
        global hist_atend
        hist_atend = store_nivel(hist_atend, df, populacao, nivel, anos)
        # Normalizar os valores pelo total da população
        total_populacao = populacao[str(ano)] / 1000
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
