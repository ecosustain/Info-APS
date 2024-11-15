import dash
from dash import Input, Output


def callback(app):
    @app.callback(
        [
            Output("content-title", "children"),
            Output("content-description", "children"),
        ],
        Input("_pages_location", "pathname"),
    )
    def modify_header_title(value):

        titles_and_descriptions = {
            "/": [
                "Atendimentos totais",
                "Atendimentos totais realizados nas unidades de atenção primária",
            ],
            "/atendimentos-programaticos": [
                "Atendimentos programáticos",
                "Atendimentos programáticos na Atenção Primária à Saúde (APS) são aqueles organizados dentro de programas estruturados para monitorar e tratar condições específicas de saúde, seguindo diretrizes e protocolos estabelecidos",
            ],
            "/atendimentos-nao-programaticos": [
                "Atendimentos não programáticos",
                "Atendimentos não programáticos na Atenção Primária à Saúde (APS) referem-se a consultas e cuidados que não estão vinculados a programas específicos de saúde",
            ],
        }

        return titles_and_descriptions[value]
