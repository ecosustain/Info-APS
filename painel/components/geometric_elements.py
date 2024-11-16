"""Módulo para elementos geométricos do painel"""

from dash import html

square_legend = html.Span(
    style={
        "display": "inline-block",
        "width": "8px",
        "height": "8px",
        "background-color": "#632956",
        "margin-right": "5px",
    }
)

rhombus_legend = html.Span(
    style={
        "display": "inline-block",
        "width": "8px",
        "height": "8px",
        "background-color": "#34679A",
        "transform": "rotate(45deg)",
        "margin-right": "5px",
    }
)
