"""Página em dash que apresenta um compartivo entre um município e o seu estado."""

import pandas as pd
from dash import dcc, html
from funcoes import get_columns

# Ler o arquivo CSV
df = pd.read_csv("data/producao.csv")

# Pegar a lista de municípios únicos
municipios = df["Municipio"].unique()

# layout apenas com um texto
layout = html.Div([html.H1("Comparativo de Atendimento Básico de Saúde")])

# Função para registrar os callbacks
