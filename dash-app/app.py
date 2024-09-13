from dash import Dash, html, dcc
from components.dropdowns import create_location_dropdowns
from components.graph import create_graph
from components.map import create_map
from callbacks import update_dropdown, update_bar_graph, update_map_graph, update_dropdown_map, update_static_page, \
    data_download
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from components.layout import layout


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.prevent_initial_callbacks = 'initial_duplicate'
# Layout do App
# app.layout = html.Div([
#     dcc.Store(id='initial-load'),  # Armazena o estado da carga inicial
#     create_location_dropdowns(),
#     create_graph(),
#     create_map()
# ])

server = app.server
# Define o layout da aplicação
app.layout = layout
# Registrando callbacks
update_dropdown.register_callbacks(app)
update_bar_graph.register_callbacks(app)
update_dropdown_map.register_callbacks(app)
update_map_graph.register_callbacks(app)
# data_download.register_callbacks(app)
# update_static_page.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
