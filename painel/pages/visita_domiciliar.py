import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Tab(
            label="Visita Domiciliar",
            value="tab-visitas",
            children=[
                dbc.Row(
                    html.H3(
                        "Visitas Domiciliar",
                        className="text-start ms-0, mb-3",
                        id="section-visitas",
                    )
                ),
                dbc.Row(
                    [
                        # Atendimento por visitas domiciliar por trimestre
                        dbc.Col(
                            dcc.Graph(
                                id="chart_visitas_by_year",
                                style={"height": "40vh"},
                            ),
                            width=3,
                        ),
                        # Atendimento por visitas domiciliar por trimestre
                        dbc.Col(
                            dcc.Graph(
                                id="chart_visitas_by_quarter",
                                style={"height": "40vh"},
                            ),
                            width=9,
                        ),
                    ],
                    className="mb-3",
                ),
            ],
        ),
    ]
)
