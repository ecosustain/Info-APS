import pandas as pd
from dash import dcc, html
from funcoes import get_columns, normaliza_por_estado

# Ler o arquivo CSV
df = pd.read_csv("data/producao.csv")
populacao = pd.read_csv("data/populacao.csv")
colunas = get_columns()

# Normalizar os dados por estado
df_normalizado = normaliza_por_estado(df, populacao)

options = []
for key, values in colunas.items():
    for value in values:
        options.append({"label": f"{key} - {value}", "value": value})

# Layout da página Painel Anual
layout = html.Div(
    [
        html.H1("Painel Avançado de Atendimento Básico de Saúde"),
        html.Label("Selecione a Coluna:"),
        dcc.Dropdown(
            id="dropdown-coluna",
            options=options,
            value=options[0]["value"],
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
        dcc.Graph(id="mapa-estado"),
    ]
)


def init_callbacks(app):
    from callbacks.mapa_callbacks import register_callbacks

    register_callbacks(app)
