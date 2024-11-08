import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(
    __name__,
    path="/atendimentos-nao-programaticos",
    title="Não Programáticos",
    name="Não Programáticos",
)

layout = html.Div(
    [
        dcc.Tab(
            label="Não Programáticos",
            value="tab-naoprogramaticos",
            children=[
                dbc.Row(
                    html.H3(
                        "Em construção",
                        className="text-start ms-0, mb-3",
                        id="section-naoprogramaticos",
                    )
                ),
                
            ],
        ),
    ]
)
