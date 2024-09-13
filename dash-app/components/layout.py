from dash import dcc, html
import dash_bootstrap_components as dbc

from components.download_button import create_download_button
from components.dropdowns import create_location_dropdowns, create_dropdowns_map, create_category_dropdowns
from components.graph import create_graph
from components.header import header_section
from components.map import create_map
from components.topbar import navbar
# Layout principal da aplicação
layout = html.Div([
    # Navbar
    navbar,
    # Header Section
    header_section,
    # Abas com gráficos e filtros
    dcc.Tabs([
        dcc.Tab(label='Produção', value='localizacao', children=[
            html.Div([
                dcc.Store(id='initial-load'),
                html.Div([
                    create_location_dropdowns(),
                    ]
                , style={'width': '25%', 'display': 'inline-block', 'paddingRight': '10px'}),
                html.Div([
                    create_category_dropdowns(),
                    create_graph()],
                    style={'width': '75%', 'display': 'inline-block'}),
            ], style={'display': 'flex'}),
        ]),
        dcc.Tab(label='Mapa', value='categorias', children=[
            html.Div([
                html.Div([
                    dcc.Store(id='initial-load-map'),
                    create_dropdowns_map(),
                ], style={'width': '25%', 'display': 'inline-block', 'paddingRight': '10px'}),
                html.Div(create_map(), style={'width': '75%', 'display': 'inline-block'})
            ], style={'display': 'flex'})
        ])
    ], id='tabs', value='localizacao', style={'padding': '20px', 'backgroundColor': '#f0f2f5'}),

], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#F0F2F5', 'height': '100vh'})
#style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#e0e0e0', 'height': '100vh'})