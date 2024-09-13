from dash import html, dcc


def create_location_dropdowns():
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='region-dropdown',
                options=[],
                placeholder="Selecione a Região",
                className="m-4",
                multi=True,
            ),
            dcc.Dropdown(
                id='state-dropdown',
                options=[],
                placeholder="Selecione um Estado",
                className="m-4",
                multi=True,
            ),
            dcc.Dropdown(
                id='city-dropdown',
                options=[],
                placeholder="Selecione os Municípios",
                className="m-4",
                multi=True,

            ),
        ], className='dropdowns')
    ])
def create_category_dropdowns():
    return html.Div([
        dcc.Dropdown(
            id='activity-dropdown',
            options=[],
            placeholder="Selecione a Atividade",
            className="m-4",
            multi=True,
        ),
        dcc.Dropdown(
            id='category-dropdown',
            options=[],
            placeholder="Selecione as Categorias",
            className="m-4",
            multi=True,

        )
    ], className='dropdowns')


def create_dropdowns_map():
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='activity-dropdown-map',
                options=[],
                placeholder="Selecione a Atividade",
                className="m-4",
                multi=True,
            ),

            dcc.Dropdown(
                id='category-dropdown-map',
                options=[],
                placeholder="Selecione as Categorias",
                className="m-4",
                multi=True,

            ),
            dcc.Dropdown(
                id='year-dropdown-map',
                options=[],
                placeholder="Selecione o ano",
                className="m-4",
                multi=True,

            ),
        ], className='dropdowns')
    ])
