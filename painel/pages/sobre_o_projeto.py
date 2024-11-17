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

def section_description(title, description):
    return dbc.Col([
        html.Div([
            html.Img(
                src=dash.get_asset_url("sisab-dark.svg"),
                height="20px",
                style={"padding-right": "12px"},
            ),
            html.H2(
                title,
                className="about-title",
                style={"font-size": "20px", "padding": "20px 0px 8px"}
            ),
        ], style={"display": "flex", "align-items": "center", "min-height": "85px"}),
        html.P(
            description,
            className="about-description",
            style={"font-size": "12px", "padding": "0px 12px"}
        ),
    ], style={"padding": "0px 15px"})

def iesp_people(name, function, image):

    return dbc.Col([
        html.Img(
            src=dash.get_asset_url(image),
            className="ieps-people",
            height="120",
        ),
        html.P(
            name,
            className="people-name",
        ),
        html.P(
            function,
            className="people-function",
        ),
    ], style={"justify-items": "center"})

def usp_people(name, function, image):

    return dbc.Col([
        html.Img(
            src=dash.get_asset_url(image),
            className="ieps-people usp",
            height="120",
        ),
        html.P(
            name,
            className="people-name usp",
        ),
        html.P(
            function,
            className="people-function usp",
        ),
    ], style={"justify-items": "center"})

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
            ], style={"padding": "0px 25px 0px 60px"}),
            html.Img(
                src=dash.get_asset_url("page_overview.png"),
                className="site-image"
            ),
        ], style={"display": "flex", "justify-content": "space-between", "margin-bottom": "60px", "align-items": "center"}),
        dbc.Row([
            section_description(
              "Atendimentos não programáticos",
              "Atendimentos não programáticos na Atenção Primária à Saúde (APS) referem-se a consultas e cuidados que não estão vinculados a programas específicos de saúde, como pré-natal, controle de hipertensão ou diabetes, mas que atendem às demandas espontâneas e variadas da população. Esses atendimentos incluem, por exemplo, queixas agudas, condições crônicas não priorizadas em programas, acompanhamento de problemas de saúde mental ou qualquer outra necessidade apresentada pelo paciente durante sua visita à unidade de saúde. Eles desempenham um papel essencial no acolhimento e na resolutividade das demandas individuais, garantindo a integralidade do cuidado."
            ),
            section_description(
              "Atendimentos totais",
              "Atendimentos totais realizados nas unidades de atenção primária."
            ),
            section_description(
              "Atendimentos programáticos",
              "Atendimentos programáticos na Atenção Primária à Saúde (APS) são aqueles organizados dentro de programas estruturados para monitorar e tratar condições específicas de saúde, seguindo diretrizes e protocolos estabelecidos. Exemplos incluem o pré-natal, o acompanhamento de crianças, e o controle de doenças crônicas como hipertensão e diabetes. Esses atendimentos têm como objetivo promover a continuidade e a qualidade do cuidado, garantindo que as condições prioritárias de saúde sejam abordadas de forma planejada e sistemática."
            ),
        ], style={"margin": "0px 60px 60px"}),
        html.Div([
            html.Div([
                html.Div([
                    html.Img(
                        src=dash.get_asset_url("logodash-amarelo.svg"),
                        height="35px",
                        style={"padding-right": "12px"},
                    ),
                    html.H2(
                        "Sobre o Instituto - IEPS",
                        className="about-title",
                        style={"color": "#ffc20d", "margin": "0px"}
                    ),
                ], style={"display": "flex", "align-items": "center", "margin-bottom": "8px"}),
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
                    dbc.Row([
                        iesp_people("Leonardo Rosa", "Pesquisador IEPS", "leonardorosa.png"),
                        iesp_people("Helena Arruda", "Pesquisadora IEPS", "helena.jpeg"),
                        iesp_people("Vinícius Peçanha", "Pesquisador IEPS", "vinicius_pecanha.jpg"),
                    ], style={"display": "flex", "gap": "30px", "padding": "0px 25px"})
                ])
            ], )
        ], className="about-ieps"),
        html.Div([
            html.Div([
                html.H2(
                    "Sobre o desenvolvimento",
                    className="about-title",
                    style={"color": "#343A40"}
                ),
                html.P(
                    "Sobre o desenvolvimento",
                    className="about-description",
                ),
            ]),
            html.Div([
                html.H2(
                    "Equipe de analistas de dados",
                    className="about-title",
                    style={"font-size": "20px", "color": "#343A40", "padding": "20px 0px 8px"}
                ),
                dbc.Row([
                    usp_people("Daniel Schulz", "Analista de dados", "daniel.png"),
                    usp_people("Elinilson Vital", "Analista de dados", "vital.png"),
                    usp_people("Mariana Cruvinel", "Analista de dados", "mariana.png"),
                    usp_people("Leonardo Gomes", "Analista de dados", "leonardo.png"),
                    usp_people("Lucas Macedo", "Analista de dados", "lucas.png"),
                ], style={"gap": "30px", "padding": "0px 25px"})
            ])
        ], className="about-dev"),
        html.Div (
            [
                html.Img(
                    src=dash.get_asset_url("logodash.svg"),
                ),
            ], className="image-bottom"
        )
    ],
    style={"padding": "50px 0px 0px 0px"},
)