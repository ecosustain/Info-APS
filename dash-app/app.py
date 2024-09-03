from dash import Dash, html, dcc
from components.header import create_header
from components.dropdowns import create_dropdowns
from components.graph import create_graph
from callbacks import update_dropdown, update_graph
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout do App
app.layout = html.Div([
    dcc.Store(id='initial-load'),  # Armazena o estado da carga inicial
    create_header(),
    create_dropdowns(),
    create_graph()
])

# Registrando callbacks
update_dropdown.register_callbacks(app)
update_graph.register_callbacks(app)
# update_map.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
