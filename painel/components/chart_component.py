from dash import dcc, html

import dash_bootstrap_components as dbc

def chart_component(title, chart_id, tag_text, icon=None):
    icon_content = html.Div([])

    if icon != None:
        icon_content = html.Span(
            id=f"{chart_id}-icon",
            className=f"fa fa-{icon} icon-indicator",
            style={
                "color": "#632956",
                "background-color": "#6329561a",
                "border": "1px solid #632956",
            },
        )
        
    return dbc.Col(
        [
            html.Div(
                [
                    html.H2(
                        title,
                        id="chart-title",
                    ),
                    icon_content
                ], style= {"display": "flex", "justify-content": "space-between"}
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