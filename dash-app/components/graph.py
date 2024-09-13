from dash import html, dcc

def create_graph():
    return html.Div([
        html.Div(children=[
        dcc.Loading(
            id="loading-bar",
            type="default",
            children=[
                dcc.Graph(id='bar-chart')
            ]
        )
        ])
  ])