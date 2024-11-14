from dash import dcc, html

import dash_bootstrap_components as dbc

def chart_component(title, chart_id, tag_text):
    return dbc.Col(
        [
            html.H2(
                title,
                id="chart-title",
            ),
            html.Span(
                tag_text,
                id=f"tag-{chart_id}",
                className="tag-chart rounded",
            ),
            dcc.Graph(
                id=chart_id,
                style={"height": "35vh"},
                clear_on_unhover=True,
            ),
        ],
        className="content-chart-box",
    )