from dash import html

import dash_bootstrap_components as dbc

slash_column = dbc.Col(
    [
        html.Span(
            style={
                "display": "inline-block",
                "width": "1px",
                "height": "100%",
                "background-color": "#212529bf",
            }
        )
    ],
    className="slash",
)