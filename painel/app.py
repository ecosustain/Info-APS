import dash
from flask import Flask
from dash import html, dcc
from paginas import painel_anual, mapa

# Flask server
server = Flask(__name__)

# Dash app
app = dash.Dash(__name__, server=server)

# Layout da aplicação principal
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback para troca de páginas
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/painel-anual':
        return painel_anual.layout
    elif pathname == '/mapa':
        return mapa.layout
    elif pathname == '/':
        return html.Div(
            className="home-container",
            children=[
                html.H1("Página Inicial"),
                html.P("Selecione uma das opções abaixo:"),
                dcc.Link("Painel Anual", href='/painel-anual', className='home-link'),
                dcc.Link("Mapa", href='/mapa', className='home-link')
            ]
        )
    else:
        return html.H1("404 Página não encontrada")

# Registrar callbacks
painel_anual.init_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
