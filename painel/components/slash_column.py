"""Componente que representa uma barra vertical de divisão."""

import dash_bootstrap_components as dbc
from dash import html

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
