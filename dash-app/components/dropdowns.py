from dash import html, dcc

def create_dropdowns():
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='region-dropdown',
                options=[],
                placeholder="Selecione a Região",
                className="m-4",
                style={'width': '50%'}
            ),

            dcc.Dropdown(
                id='state-dropdown',
                options=[],
                placeholder="Selecione um Estado",
                className="m-4",
                style = {'width': '50%'}
    ),
            dcc.Dropdown(
                id='city-dropdown',
                options=[],
                placeholder="Selecione os Municípios",
                className="m-4",
                multi=True,
                style = {'width': '50%'}
            ),
            dcc.Dropdown(
                id='category-dropdown',
                options=[],
                placeholder="Selecione as Categorias",
                className="m-4",
                multi=True,
                style = {'width': '50%'}
            )
        ], className='dropdowns')
    ])
