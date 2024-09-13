from dash import html
import dash_bootstrap_components as dbc

header_section = html.Div([
    html.Div([
        html.H2('Projeto em Ciência de Dados', style={'fontSize': '36px', 'color': '#fff'}),
        html.P(
            "O objetivo do projeto é desenvolver uma ferramenta que auxilie gestores públicos na tomada de decisões e que sirva como uma fonte confiável de dados para pesquisas científicas na área da saúde.",
            style={'color': '#d1d1e0', 'fontSize': '20px'},
        ),
        html.P(
            "Para isso, serão coletados dados de atendimentos primários disponibilizados pelo sistema de saúde pública SISAB (https://sisab.saude.gov.br/) como fonte principal, utilizando técnicas de web scraping.",
            style={'color': '#d1d1e0', 'fontSize': '20px'}
        ),
        html.P(
            "Os dados coletados serão processados, incluindo limpeza, complementação e avaliação de consistência por especialistas. Em seguida, os dados serão rotulados e organizados em relatórios interativos com gráficos e tabelas dinâmicas.",
            style={'color': '#d1d1e0', 'fontSize': '20px'}
        ),
        html.P(
            "Esses relatórios serão disponibilizados em um painel web com uma interface intuitiva e recursos avançados de visualização para facilitar a interpretação e o uso das informações.",
            style={'color': '#d1d1e0', 'fontSize': '20px'},
        ),
        html.P(
            "O projeto esta sendo desenvolvido no contexto da matéria MAC476 | 6967 - Laboratório Avançado de Ciência de Dados (2024), do curso da Ciência de Computação - IME USP",
            style={'color': '#d1d1e0', 'fontSize': '20px'},
        ),
        html.Div([
            # dbc.Button('Colaboradores', color="info", className="me-2"),
            # dbc.Button('See a Random Material', color="secondary", className="me-2"),
            # dbc.Button('Browse Apps', color="secondary", className="me-2"),
        ], style={'marginTop': '20px'})
    ], style={'padding': '40px', 'backgroundColor': '#323d61'})
])
