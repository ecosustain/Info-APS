import dash.dependencies as dd
import plotly.express as px
from funcoes import cria_mapa_uf
from paginas.mapa import df_normalizado


def register_callbacks(app):
    """Função para registrar os callbacks"""

    @app.callback(
        dd.Output("mapa-estado", "figure"),
        [
            dd.Input("dropdown-coluna", "value"),
            dd.Input("slider-ano", "value"),
        ],
    )
    def update_map(coluna, ano):
        data_inicio = f"{ano}-01-01"
        data_fim = f"{ano}-12-31"
        mapa_uf = cria_mapa_uf(df_normalizado, data_inicio, data_fim)

        # Plotar o mapa para uma coluna específica, por exemplo, 'Asma'
        fig = px.choropleth(
            mapa_uf,
            geojson=mapa_uf.geometry,  # Usar a geometria do shapefile
            locations=mapa_uf.index,
            color=coluna,  # Coluna que queremos mapear
            color_continuous_scale="reds",
            title=f"Atendimentos de {coluna} por Estado no Brasil - 2023",
        )

        # Ajustar as configurações do mapa
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

        return fig
