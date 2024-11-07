import dash_bootstrap_components as dbc

from callbacks.api_requests import get_anos
from callbacks.utils import estados_brasileiros

from dash import dcc, html

anos = get_anos(6)

def Header():
  return html.Div(
    id="header",
    children=[
        dbc.Row(
          [
              dbc.Col(
                  dcc.Dropdown(
                      id="dropdown-estado",
                      options=[
                          {"label": estado, "value": estado}
                          for estado in estados_brasileiros
                      ],
                      placeholder="Selecione o Estado",
                      searchable=True,
                      clearable=True,  # Permite limpar a seleção
                  ),
                  width=2,
              ),
              dbc.Col(
                  dcc.Dropdown(
                      id="dropdown-regiao",
                      options=[],
                      placeholder="Selecione a Região",
                      searchable=True,
                      clearable=True,  # Permite limpar a seleção
                  ),
                  width=4,
              ),
              dbc.Col(
                  dcc.Dropdown(
                      id="dropdown-municipio",
                      options=[],
                      placeholder="Selecione o Municipio",
                      searchable=True,
                      clearable=True,  # Permite limpar a seleção
                  ),
                  width=4,
              ),
          ]
      ),
      dbc.Row(
          # breakline
          html.Br(),
      ),
      dbc.Row(
          dbc.Col(
              dbc.ButtonGroup(
                  [
                      dbc.Button(
                          str(ano),
                          id=f"btn-ano-{ano}",
                          color="primary",
                          outline=True,
                          active=(
                              ano == anos[0]
                          ),  # Define o primeiro ano como ativo
                          className="me-4 rounded",  # Adiciona margem à direita e borda arredondada
                          style={
                              "background-color": (
                                  "#A5A5A5"
                                  if ano != anos[0]
                                  else "#000000"
                              ),  # Fundo cinza claro ou escuro
                              "border-color": "#A5A5A5",  # Cor da borda
                              "color": (
                                  "#fff"
                                  if ano != anos[0]
                                  else "#00000"
                              ),  # Cor do texto
                              "padding": "0px 12px",
                          },
                      )
                      for ano in anos
                  ],
                  vertical=False,  # Para deixar os botões lado a lado
              )
          ),
          className="mb-4",
      )
    ]
  )