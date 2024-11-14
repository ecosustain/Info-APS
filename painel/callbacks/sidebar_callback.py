import dash
from dash import Input, Output

def callback(app):
    def sidebar_style(path):
        @app.callback(
            Output(f"{path}", "style"),
            Input('_pages_location', 'pathname'),
        )
        def modify_sidebar_selection(value, l):

            print("l----------------")
            print(l)

            if path == value: 
                return {
                    "background-color": "#f8f9fa",
                    "color": "#343A40"
                }
            
            return {
                "background-color": "#343A40",
                "color": "white" 
            }

    for page in dash.page_registry.values():
        sidebar_style(page['path'])
