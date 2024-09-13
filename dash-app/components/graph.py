from dash import dcc, html


def create_graph():
    return html.Div(
        [
            html.Div(
                children=[
                    dcc.Graph(id="bar-chart"),
                ]
            )
        ]
    )
