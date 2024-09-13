from dash import dcc, html

def create_map():
    return html.Div([
        dcc.Loading(
            id="loading-map",
            type="default",
            children=[
                dcc.Graph(id='map', style={'height': '600px'}),
            ]
        )

    ], className='map-container')
