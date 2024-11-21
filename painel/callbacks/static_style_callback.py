"""Módulo para callbacks do estilo estático."""

from callbacks.utils.utils import get_type
from dash import Input, Output, clientside_callback


def callback(app):
    """Função para registrar os callbacks do estilo estático"""

    def update_button_style_template(id):
        clientside_callback(
            """
            function(estado, regiao, municipio, args) {
                if (municipio) {
                    return {
                        "color": "#F7941C",
                        "background-color": "#F7941C1a",
                        "border": "1px solid #F7941C",
                    }
                }
                if (regiao) {
                    return {
                        "color": "#2B7B6F",
                        "background-color": "#2B7B6F1a",
                        "border": "1px solid #2B7B6F",
                    }
                }
                if (estado) {
                    return {
                        "color": "#34679A",
                        "background-color": "#34679A1a",
                        "border": "1px solid #34679A",
                    }
                }
                return {
                    "color": "#632956",
                    "background-color": "#6329561a",
                    "border": "1px solid #632956",
                }
            }
            """,
            Output(id, "style"),
            Input("dropdown-estado", "value"),
            Input("dropdown-regiao", "value"),
            Input("dropdown-municipio", "value"),
            Input(id, "style"),
        )

    ids = [
        "indicator-icon-tooth",
        "indicator-icon-house",
        "indicator-icon-user-doctor",
        "indicator-icon-hand-point-right",
        "chart_encaminhamentos-icon",
        "chart_by_year_profissionais-icon",
        "chart_odonto_by_year-icon",
        "chart_visitas_by_year-icon",
        "chart_odonto_by_quarter-icon",
        "chart_visitas_by_quarter-icon",
        "tag-trimestre",
        "tag-ano",
    ]

    for id in ids:
        update_button_style_template(id)
