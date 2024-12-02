"""Módulo para callbacks do header."""

from dash import Input, Output, clientside_callback

def callback(app):
    """Função para registrar os callbacks do header."""

    app.clientside_callback(
        """
        function(value) {
            if (value == "/health/primary-care/sobre_o_projeto") {
                return {"display": "none"}
            }

            return {"display": "block"}
        }
        """,
        Output("header", "style"),
        Input("_pages_location", "pathname"),
    )

    clientside_callback(
        """
        function(value) {
            var titles_and_descriptions = {
                "/health/primary-care/": [
                    "Atendimentos totais",
                    "Atendimentos totais realizados nas unidades de atenção primária",
                ],
                "/health/primary-care/atendimentos-programaticos": [
                    "Atendimentos programáticos",
                    "Atendimentos programáticos na Atenção Primária à Saúde (APS) são aqueles organizados dentro de programas estruturados para monitorar e tratar condições específicas de saúde, seguindo diretrizes e protocolos estabelecidos",
                ],
                "/health/primary-care/atendimentos-nao-programaticos": [
                    "Atendimentos não programáticos",
                    "Atendimentos não programáticos na Atenção Primária à Saúde (APS) referem-se a consultas e cuidados que não estão vinculados a programas específicos de saúde",
                ],
                "/health/primary-care/sobre_o_projeto": [
                    "Sobre o projeto",
                    "",
                ],
            }

            return titles_and_descriptions[value]
        }
        """,
        [
            Output("content-title", "children"),
            Output("content-description", "children"),
        ],
        Input("_pages_location", "pathname"),
    )
