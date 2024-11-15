import dash_bootstrap_components as dbc
from components.geometric_elements import rhombus_legend, square_legend
from dash import html


def indicator_component(title, ind_brasil, ind_estado, ind, icon):
    legend = html.Div([])
    icon_content = html.Div([])

    if ind_brasil != None:
        legend = html.Div(
            className="indicator-legend-box",
            children=[
                html.Div(
                    className="indicator-legend",
                    children=[
                        square_legend,
                        html.P(id=ind_brasil, className="legend-text"),
                    ],
                ),
                html.Div(
                    className="indicator-legend",
                    children=[
                        rhombus_legend,
                        html.P(id=ind_estado, className="legend-text"),
                    ],
                ),
            ],
        )

    if icon != None:
        icon_content = html.Div(
            [
                html.Span(
                    id=f"indicator-icon-{icon}",
                    className=f"fa fa-{icon} icon-indicator",
                    style={
                        "color": "#632956",
                        "background-color": "#6329561a",
                        "border": "1px solid #632956",
                    },
                )
            ],
        )

    return dbc.Col(
        [
            dbc.Row(
                html.H4(
                    title,
                    className="description-indicator-small",
                ),
            ),
            legend,
            dbc.Row(
                html.Div(
                    className="indicator-footer",
                    children=[
                        html.H2(
                            id=ind,
                            className="indicator-number-small",
                        ),
                        icon_content,
                    ],
                ),
            ),
        ],
        className="indicator-column",
    )
