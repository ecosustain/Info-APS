"""Módulo para callbacks do sidebar."""

import dash
from dash import Input, Output


def callback(app):
    """Função para registrar os callbacks do sidebar"""

    def sidebar_style(path):
        @app.callback(
            Output(f"{path}", "style"),
            Input("_pages_location", "pathname"),
        )
        def modify_sidebar_selection(value):
            """Função para modificar o estilo do item selecionado no sidebar"""
            if path == value:
                return {"background-color": "#f8f9fa", "color": "#343A40"}

            return {"background-color": "#343A40", "color": "white"}

    for page in dash.page_registry.values():
        sidebar_style(page["path"])
