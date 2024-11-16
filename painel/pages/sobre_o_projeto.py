import dash
import dash_bootstrap_components as dbc
from api.api_requests import anos
from components.chart_component import chart_component
from components.geometric_elements import rhombus_legend, square_legend
from components.indicator_component import indicator_component
from components.map import Map
from components.slash_column import slash_column
from dash import dcc, html

dash.register_page(__name__, path="/")
dash.register_page(
    __name__,
    path="/sobre_o_projeto",
    title="Sobre o projeto",
    name="Sobre o projeto",
    order=0
)

layout = html.Div(
    [
        html.Div([
            html.Div([
                html.H2(
                    "Sobre Info-APS",
                    className="about-title",
                ),
                html.P(
                    "Sobre Info-APS",
                    className="about-description",
                ),
            ], style={"padding": "0px 25px"}),
            html.Img(
                src=dash.get_asset_url("page_overview.png"),
                className="site-image"
            ),
        ], style={"display": "flex", "justify-content": "space-between", "margin-bottom": "60px"}),
        html.Div([
            html.Div([
                html.H2(
                    "Sobre o Instituto - IEPS",
                    className="about-title",
                    style={"color": "#ffc20d"}
                ),
                html.P(
                    "O Instituto de Estudos para Políticas de Saúde (IEPS) é uma organização sem fins lucrativos, independente e apartidária. Nosso objetivo é contribuir para o aprimoramento das políticas públicas para a saúde no Brasil. Defendemos a ideia de que toda a população brasileira deva ter acesso à saúde de qualidade e que o uso de recursos e a regulação do sistema de saúde sejam os mais efetivos possíveis. Defendemos também que o acesso à saúde respeite o princípio da equidade, tendo o Estado Brasileiro um papel relevante, de natureza distributiva, neste processo.  Acreditamos que a melhor maneira de alcançar o nosso propósito é por meio de políticas públicas baseadas em evidências, desenhadas, implementadas e monitoradas de maneira transparente – sempre buscando o apoio da sociedade.",
                    className="about-description",
                    style={"color": "#ffffffab"}
                ),
                html.Div([
                    html.H2(
                        "Equipe IEPS",
                        className="about-title",
                        style={"font-size": "20px", "color": "#ffc20d", "padding": "20px 0px 8px"}
                    ),
                    html.Div([
                        html.Div([
                            html.Img(
                                src=dash.get_asset_url("leonardorosa.png"),
                                className="ieps-people",
                                height="120"
                            ),
                            html.P(
                                "Leonardo Rosa",
                                className="people-name",
                            ),
                            html.P(
                                "Pesquisador IEPS",
                                className="people-function",
                            ),
                        ]),
                        html.Div([
                            html.Img(
                                src=dash.get_asset_url("helena.jpeg"),
                                className="ieps-people",
                                height="120"
                            ),
                            html.P(
                                "Helena Arruda",
                                className="people-name",
                            ),
                            html.P(
                                "Pesquisadora IEPS",
                                className="people-function",
                            ),
                        ]),
                        html.Div([
                            html.Img(
                                src=dash.get_asset_url("vinicius_pecanha.jpg"),
                                className="ieps-people",
                                height="120"
                            ),
                            html.P(
                                "Vinícius Peçanha",
                                className="people-name",
                            ),
                            html.P(
                                "Pesquisador IEPS",
                                className="people-function",
                            ),
                        ]),
                    ], style={"display": "flex", "gap": "30px", "padding": "0px 25px"})
                ])
            ], )
        ], className="about-ieps")
    ],
    style={"padding": "50px 0px 0px 0px"},
)