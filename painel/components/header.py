import dash
import dash_bootstrap_components as dbc
from callbacks.utils.utils import estados_brasileiros
from constants import time_division
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
                                "Info-APS",
                                className="text-start ms-0, mb-3",
                                id="dashboard-title",
                            ),
                            html.P(
                                "Informações de produção da atenção primária brasileira.",
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
                id="content-header",
                children=[
                    html.Div(
                        [
                            html.H2(
                                "Atendimentos totais",
                                id="content-title",
                                style={"font-size": "20px"},
                            ),
                            html.P(
                                "Atendimentos totais realizados nas unidades de atenção primária",
                                id="content-description",
                                style={
                                    "font-size": "11px",
                                    "line-height": "14px",
                                    "color": "#212529bf",
                                    "margin": "0px",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "flex-direction": "column",
                            "justify-content": "center",
                        },
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
                                                active=(
                                                    division
                                                    == time_division.graphic_division[
                                                        0
                                                    ]
                                                ),  # Define o primeiro ano como ativo
                                                className="temp-button rounded",
                                                style={"padding": "0px"},
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
            ),
        ],
    )
