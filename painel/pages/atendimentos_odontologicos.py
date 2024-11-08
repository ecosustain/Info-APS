import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(
    __name__,
    path="/atendimentos-odontologicos",
    title="Atendimentos Odontológicos",
    name="Atendimentos Odontológicos",
)

layout = html.Div(
    [
        dcc.Tab(
            label="Atendimentos Odontológicos",
            value="tab-odonto",
            children=[
                dbc.Row(
                    html.H3(
                        "Atendimentos Odontológicos",
                        className="text-start ms-0, mb-3",
                        id="section-odontologicos",
                    )
                ),
                dbc.Row(
                    [
                        # Atendimento por atendimentos odontologicos por trimestre
                        dbc.Col(
                            dcc.Graph(
                                id="chart_odonto_by_quarter",
                                style={"height": "40vh"},
                            ),
                            width=12,
                        ),
                    ],
                    className="mb-3",
                ),
            ],
        ),
    ]
)
