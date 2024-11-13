# callbacks/update_tables.py
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from data.database import Database
from sklearn.preprocessing import MinMaxScaler
from utils.queries import (GET_DATA_BY_CATEGORY, GET_DATA_BY_CITY,
                           GET_DATA_BY_REGION, GET_DATA_BY_STATE)


def register_callbacks(app):
    @app.callback(
        Output("bar-chart", "figure"),
        [
            Input("region-dropdown", "value"),
            Input("state-dropdown", "value"),
            Input("city-dropdown", "value"),
            Input("category-dropdown", "value"),
        ],
    )
    def update_graph(region, state, city, category):
        db = Database()
        db.connect()
        data = None

        if (
            region is not None
            and state is None
            and city is None
            and category is None
        ):
            data = db.fetch_data(GET_DATA_BY_REGION, (region,))

        if (
            region is not None
            and state is not None
            and city is None
            and category is None
        ):
            data = db.fetch_data(GET_DATA_BY_STATE, (state,))

        if (
            region is not None
            and state is not None
            and city is not None
            and category is None
        ):
            data = db.fetch_data(GET_DATA_BY_CITY, (city,))

        if (
            region is not None
            and state is not None
            and city is not None
            and category is not None
        ):
            data = db.fetch_data(
                GET_DATA_BY_CATEGORY,
                (
                    city,
                    category,
                ),
            )

        db.close()

        # Check if data is not None and convert to DataFrame
        if data:
            # Assumindo que os dados retornados são tuplas e o banco retorna colunas 'name' e 'total'
            df = pd.DataFrame(
                data, columns=["name", "total", "geo_unit", "year"]
            )
        else:
            # Criando um DataFrame vazio se os dados forem None ou vazios
            df = pd.DataFrame(columns=["name", "total", "geo_unit", "year"])

        # # Inicializa o MinMaxScaler para normalizar os dados entre 0 e 1
        # scaler = MinMaxScaler()
        #
        # # Normaliza a coluna 'total'
        # df['total'] = scaler.fit_transform(df[['total']])

        # Criar o gráfico de barras com Plotly
        fig = px.bar(
            df,
            x="year",
            y="total",
            color="name",
            height=800,
        )

        # Atualizar os labels dinamicamente com base no contexto dos dados
        fig.update_layout(
            xaxis_title=f"Ano",
            yaxis_title="Total",
            # template='plotly_white',
            # xaxis_tickangle=-45,
        )
        return fig
