import dash
from dash import Input, Output

from api.api_requests import (
    anos,
)

def callback(app):
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