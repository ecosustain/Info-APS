import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(
    __name__,
    path="/atendimentos-programaticos",
    title="Programáticos",
    name="Programáticos",
)

layout = html.Div(
    [
        dcc.Tab(
            label="Programáticos",
            value="tab-programaticos",
            children=[
                dbc.Row(
                    html.H3(
                        "Em construção",
                        className="text-start ms-0, mb-3",
                        id="section-programaticos",
                    )
                ),
                
            ],
        ),
    ]
)
