# callbacks/update_tables.py
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from data.database import Database
from utils.queries import GET_DATA_BY_REGION, GET_DATA_BY_STATE, GET_DATA_BY_CITY, GET_DATA_BY_CATEGORY, \
    GET_DATA_BY_REGION_ALL, GET_DATA_BY_ACTIVITY
from sklearn.preprocessing import MinMaxScaler

from utils.validation import is_valid


def register_callbacks(app):

    @app.callback(
        Output('bar-chart', 'figure'),
        [
            Input('region-dropdown', 'value'),
            Input('state-dropdown', 'value'),
            Input('city-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('activity-dropdown', 'value'),
         ]
    )

    def update_bar_graph(region, state, city, category, activity):

        db = Database()
        db.connect()
        data = None

        is_region = is_valid(region)
        is_state = is_valid(state)
        is_city = is_valid(city)
        is_category = is_valid(category)
        is_activity = is_valid(activity)

        if is_activity:
            if not is_region:
                region = None
            if not is_state:
                state = None
            if not is_city:
                city = None
            if not is_category:
                category = None
            data = db.fetch_data(GET_DATA_BY_ACTIVITY, (activity, region,region, state,state, city, city, category,  category, ))
        else:
            if not is_region :
                data = db.fetch_data(GET_DATA_BY_REGION_ALL)

            if is_region and not is_state and not is_city and not is_category:
                data = db.fetch_data(GET_DATA_BY_REGION, (region,))

            if is_region and is_state and not is_city and not is_category:
                data = db.fetch_data(GET_DATA_BY_STATE, (state,))

            if is_region and is_state and is_city and not is_category:
                data = db.fetch_data(GET_DATA_BY_CITY, (city,))

        db.close()

        return update_bar_fig(data)

    def update_bar_fig(data):
        # Check if data is not None and convert to DataFrame
        if data:
            # Assumindo que os dados retornados são tuplas e o banco retorna colunas 'name' e 'total'
            df = pd.DataFrame(data, columns=['name', 'total', 'geo_unit', 'year'])
        else:
            # Criando um DataFrame vazio se os dados forem None ou vazios
            df = pd.DataFrame(columns=['name', 'total', 'geo_unit', 'year'])
        # Criar o gráfico de barras com Plotly
        fig = px.bar(
            df,
            x='year',
            y='total',
            color='name',
        )
        # Atualizar os labels dinamicamente com base no contexto dos dados
        fig.update_layout(
            xaxis_title=f"Ano",
            yaxis_title="Total",
            # template='plotly_white',
            # xaxis_tickangle=-45,
        )
        return fig
