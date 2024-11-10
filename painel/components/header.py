import dash
import dash_bootstrap_components as dbc
from constants import time_division
from callbacks.utils import estados_brasileiros
from dash import dcc, html

def Header():
    return html.Div(
        id="header",
        children=[
            html.Div(
                id="header-title",
                children=[
                    html.Div(
                        id="header-description",
                        children=[
                            html.H3(
                                "DASHBOARD",
                                className="text-start ms-0, mb-3",
                                id="dashboard-title",
                            ),
                            html.P(
                                "Esse dashboard tem como objetivo democratizar as informações da saúde pública do Brasil coletadas pelo SISAB.",
                                className="text-start ms-0, mb-3",
                                id="dashboard-description",
                            ),
                        ],
                    ),
                    html.Div(
                        id="header-symbol",
                        children=[
                            html.Img(
                                src=dash.get_asset_url("logodash.svg"),
                                height="30px",
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="header-filter",
                children=[
                    html.Div(
                        id="filter-dropdown",
                        children=[
                            dcc.Dropdown(
                                id="dropdown-estado",
                                className="dropdown",
                                options=[
                                    {"label": estado, "value": estado}
                                    for estado in estados_brasileiros
                                ],
                                placeholder="Selecione o Estado",
                                searchable=True,
                                clearable=True,  # Permite limpar a seleção
                            ),
                            dcc.Dropdown(
                                id="dropdown-regiao",
                                className="dropdown",
                                options=[],
                                placeholder="Selecione a Região",
                                searchable=True,
                                clearable=True,  # Permite limpar a seleção
                            ),
                            dcc.Dropdown(
                                id="dropdown-municipio",
                                className="dropdown",
                                options=[],
                                placeholder="Selecione o Municipio",
                                searchable=True,
                                clearable=True,  # Permite limpar a seleção
                            ),
                        ],
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.ButtonGroup(
                                [
                                    dbc.Button(
                                        str(division),
                                        id=f"btn-{division}",
                                        color="primary",
                                        outline=True,
                                        active=(
                                            division == time_division.graphic_division[0]
                                        ),  # Define o primeiro ano como ativo
                                        className="temp-button rounded",
                                        style={"padding": "0px"}
                                    )
                                    for division in time_division.graphic_division
                                ],
                                vertical=False,  # Para deixar os botões lado a lado
                            ),
                        ),
                    ),
                ],
            ),
        ],
    )
