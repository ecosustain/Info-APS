from dash import dcc, html
from funcoes import get_columns, producao

# Ler o arquivo CSV
df = producao
colunas = get_columns()

# Pegar a lista de municípios únicos
municipios = df["Municipio"].unique()

# Layout da página Painel Anual
layout = html.Div(
    [
        html.H1("Painel Avançado de Atendimento Básico de Saúde"),
        html.Label("Selecione a Coluna:"),
        dcc.Dropdown(
            id="dropdown-grupo",
            options=[
                {"label": grupo, "value": grupo} for grupo in colunas.keys()
            ],
            value="Problemas",
        ),
        html.Label("Selecione o Município:"),
        dcc.Dropdown(
            id="dropdown-municipio",
            options=[
                {"label": municipio, "value": municipio}
                for municipio in municipios
            ],
            value="SÃO PAULO",
        ),
        html.Label("Selecione o Ano:"),
        dcc.Slider(
            id="slider-ano",
            min=df["Ano"].min(),
            max=df["Ano"].max(),
            step=1,
            value=df["Ano"].max(),
            marks={str(ano): str(ano) for ano in df["Ano"].unique()},
        ),
        dcc.Graph(id="grafico-evolucao-problemas"),
        dcc.Graph(id="grafico-problemas-resumo"),
    ]
)


# Função para registrar os callbacks
def init_callbacks(app):
    """Função para registrar os callbacks"""
    from callbacks.painel_anual_callbacks import register_callbacks

    register_callbacks(app)