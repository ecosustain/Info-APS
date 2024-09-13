from dash import dcc, html

# Barra de navegação com links para as páginas
navtabs = dcc.Tabs([
    dcc.Tab(label='Localização', value='localizacao', children=[
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='localizacao-dropdown',
                    options=[
                        {'label': loc, 'value': loc} for loc in ['Cidade A', 'Cidade B', 'Cidade C', 'Cidade D']
                    ],
                    placeholder='Selecione a Localização',
                    value=None
                )
            ], style={'width': '25%', 'display': 'inline-block', 'paddingRight': '10px'}),

            html.Div(id='localizacao-graph', style={'width': '75%', 'display': 'inline-block'})
        ], style={'display': 'flex'})
    ]),

    dcc.Tab(label='Categorias', value='categorias', children=[
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='categorias-dropdown',
                    options=[
                        {'label': cat, 'value': cat} for cat in ['Cat 1', 'Cat 2']
                    ],
                    placeholder='Selecione a Categoria',
                    value=None
                )
            ], style={'width': '25%', 'display': 'inline-block', 'paddingRight': '10px'}),

            html.Div(id='categorias-graph', style={'width': '75%', 'display': 'inline-block'})
        ], style={'display': 'flex'})
    ])
], id='tabs', value='localizacao', style={'padding': '20px', 'backgroundColor': '#f0f2f5'}),
