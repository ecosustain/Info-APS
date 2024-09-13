from dash import Input, Output
from pages import about

# Callback para atualizar o conteúdo da página com base na URL

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        if pathname == '/about':
            return about.layout
