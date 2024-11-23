"""Módulo para callbacks do sidebar."""

import dash
from dash import Input, Output, clientside_callback


def callback(app):
    """Função para registrar os callbacks do sidebar"""

    def sidebar_style(path):

        clientside_callback(
            """
            function(id, value) {
                if (id == value) {
                    return {"background-color": "#f8f9fa", "color": "#343A40"}
                }

                return {"background-color": "#343A40", "color": "white"}
            }
            """,
            Output(f"{path}", "style"),
            Input(f"{path}", "id"),
            Input("_pages_location", "pathname"),
        )

    for page in dash.page_registry.values():
        sidebar_style(page["path"])
