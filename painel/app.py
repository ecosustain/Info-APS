import dash
from dash import dcc, html
import dash.dependencies as dd
import plotly.graph_objects as go
import pandas as pd
from flask import Flask

# Flask server
server = Flask(__name__)

# Dash app
app = dash.Dash(__name__, server=server)

# Ler o arquivo CSV
df = pd.read_csv("data/producao.csv")

# Dicionário de grupos de colunas
colunas = {
    'Problemas': [
        "Asma", "Desnutrição", "Diabetes", "DPOC", "Hipertensão arterial",
        "Obesidade", "Pré-natal", "Puericultura", "Puerpério (até 42 dias)",
        "Saúde sexual e reprodutiva", "Tabagismo", "Usuário de álcool",
        "Usuário de outras drogas", "Saúde mental", "Reabilitação",
        "D.Transmissíveis - Dengue", "Doenças transmissíveis - DST",
        "D.Transmissíveis - Hanseníase", "D.Transmissíveis - Tuberculose",
        "Rast. câncer de mama", "Rast. câncer do colo do útero", "Rast. risco cardiovascular"
    ],
    'Condutas Odontológicas': [
        "Agendamento p/ grupos", "Agendamento p/ outros profissi",
        "Encaminhamento - Cirurgia BMF", "Encaminhamento - Endodontia",
        "Encaminhamento - Estomatologia", "Encaminhamento - Implantodonti",
        "Encaminhamento - Odontopediatr", "Encaminhamento - Ortodontia/Or",
        "Encaminhamento - Outros", "Encaminhamento - Pacientes com",
        "Encaminhamento - Periodontia", "Encaminhamento - Prótese dentá",
        "Encaminhamento - Radiologia"
    ],
    'Condutas': [
       'Agendamento para grupos',
       'Encaminhamento interno no dia', 'Encaminhamento intersetorial',
       'Encaminhamento p/ CAPS', 'Encaminhamento p/ internação h',
       'Encaminhamento p/ serviço de a', 'Encaminhamento p/ serviço espe',
       'Encaminhamento p/ urgência'
    ],
    'Procedimentos': [
        "Acuputura - ins. de agulhas", "Adm.  med. via endovenosa", "Adm.  med. via intramuscular",
        "Adm. Med. inalação/nebulização", "Adm. Med. via tópica", "Adm. med. via Subcutânea (SC)",
        "Adm. med. via oral", "Adm. penicilina p/ tto sífilis",
        "Caut. química pequenas lesões", "Cir. de unha (cantoplastia)",
        "Col. de cito. De colo uterino", "Col. mat. p/ ex. laboratorial", 
        "Exérese/biopsia/punção de tum.", "Fundoscopia",
        "Infiltração em cav. sinovial",
        "Rem. Corp. Estranho Subcutâneo", 
        "Rm. C. Est. Cav Auditiva/Nasal", "TERAPIA DE REIDRATACAO ORAL",
        "Tes. Ráp. p/ dosg. proteinúria"
    ],
    'Motivo Visita': [
        "Acomp.  Domiciliados/Acamados", "Acomp.  Pessoa c/ Diabetes", "Acomp.  Pessoa c/ Hanseníase",
        "Acomp.  Pessoa c/ Tuberculose", "Acomp.  Pessoas c/ D. Crônicas", "Acomp.  Recém-nascido",
        "Acomp. -  DPOC/Enfisema", "Acomp. - Usuário de drogas", "Acomp. Cond.  Bolsa Família",
        "Acomp. Condições de V.S.", "Acomp. PCD  ou reabilitação", "Acomp. Pessoa c/ Asma",
        "Acomp. Pessoa c/ Câncer", "Acomp. Pessoa c/ Desnutrição", "Acomp. Pessoa c/ Hipertensão",
        "Acomp. Sintomáticos Resp.", "Acomp. Usuário de álcool", "Acompanhamento - Criança",
        "Acompanhamento - Gestante", "Acompanhamento - Puérpera", "Acompanhamento - Saúde mental",
        "Acompanhamento - Tabagista", "B.A. - Cond.  Bolsa Família", "Busca ativa - Consulta",
        "Busca ativa - Exame",  "Cadastramento/Atualização",
        "Controle de Ambientes/Vetores", "Convite At.Col./Camp. Saúde", "Egresso de Internação",
        "Outros"
    ]
}

# Pegar a lista de municípios únicos
municipios = df["Municipio"].unique()

# Criar o dropdown para seleção do grupo
dropdown_grupo = dcc.Dropdown(
    id="dropdown-grupo",
    options=[{"label": grupo, "value": grupo} for grupo in colunas.keys()],
    value="Problemas",
)

# Criar o dropdown para seleção do município
dropdown_municipio = dcc.Dropdown(
    id="dropdown-municipio",
    options=[{"label": municipio, "value": municipio} for municipio in municipios],
    value="São Paulo",
)

# Criar um seletor de ano
slider_ano = dcc.Slider(
    id="slider-ano",
    min=df["Ano"].min(),
    max=df["Ano"].max(),
    step=1,
    value=df["Ano"].max(),
    marks={str(ano): str(ano) for ano in df["Ano"].unique()},
)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Painel Avançado de Atendimento Básico de Saúde"),
    html.Label("Selecione a Coluna:"),
    dropdown_grupo,
    html.Label("Selecione o Município:"),
    dropdown_municipio,
    html.Label("Selecione o Ano:"),
    slider_ano,
    dcc.Graph(id='grafico-evolucao-problemas'),
    dcc.Graph(id='grafico-problemas-resumo')
])

# Função para filtrar os dados com base nas seleções
def filter_data(municipio, ano, grupo):
    colunas_selecionadas = colunas[grupo]
    return df[(df["Municipio"] == municipio) & (df["Ano"] == ano)][colunas_selecionadas + ['Data']]

# Callback para atualizar os gráficos com base nas seleções do usuário
@app.callback(
    [dd.Output('grafico-evolucao-problemas', 'figure'),
     dd.Output('grafico-problemas-resumo', 'figure')],
    [dd.Input('dropdown-grupo', 'value'),
     dd.Input('dropdown-municipio', 'value'),
     dd.Input('slider-ano', 'value')]
)
def update_graphs(grupo, municipio, ano):
    df_filtrado = filter_data(municipio, ano, grupo)

    # Gráfico de barras empilhadas para evolução dos problemas
    fig_evolucao = go.Figure()
    colunas_selecionadas = colunas[grupo]
    
    for problema in colunas_selecionadas:
        fig_evolucao.add_trace(go.Bar(x=df_filtrado['Data'], y=df_filtrado[problema], name=problema, hovertemplate='%{y} casos'))
    fig_evolucao.update_layout(barmode='stack', title=f'Evolução {grupo} ao Longo do Ano')

    # Gráfico de barras horizontal para problemas totais no período
    problemas_totais = df_filtrado[colunas_selecionadas].sum()
    fig_resumo = go.Figure()
    fig_resumo.add_trace(
        go.Bar(
            y=problemas_totais.index,
            x=problemas_totais.values,
            orientation="h",
        )
    )
    fig_resumo.update_layout(
        title=f"{grupo} Totais no Ano",
        xaxis_title="Total de Casos",
        yaxis_title="Problemas de Saúde",
    )

    return fig_evolucao, fig_resumo


if __name__ == "__main__":
    app.run_server(debug=True)
