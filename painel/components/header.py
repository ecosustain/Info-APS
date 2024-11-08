import dash
import dash_bootstrap_components as dbc
from callbacks.api_requests import get_anos
from callbacks.utils import estados_brasileiros
from dash import dcc, html

anos = get_anos(6)


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
                                        str(ano),
                                        id=f"btn-ano-{ano}",
                                        color="primary",
                                        outline=True,
                                        active=(
                                            ano == anos[0]
                                        ),  # Define o primeiro ano como ativo
                                        className="year-button rounded",  # Adiciona margem à direita e borda arredondada
                                        style={
                                            "background-color": (
                                                "#FFFFFF"
                                                if ano != anos[0]
                                                else "#000000"
                                            ),  # Fundo cinza claro ou escuro
                                            "border-color": "#343A40",  # Cor da borda
                                            "color": (
                                                "#fff"
                                                if ano != anos[0]
                                                else "#343A40"
                                            ),  # Cor do texto
                                            "padding": "10px 12px",
                                        },
                                    )
                                    for ano in anos
                                ],
                                vertical=False,  # Para deixar os botões lado a lado
                            )
                        ),
                    ),
                ],
            ),
        ],
    )
