# callbacks/update_tables.py

from dash.dependencies import Input, Output
from data.database import Database
from utils.queries import GET_STATES, GET_REGIONS, GET_CITIES, GET_CATEGORY_BY_CITY, GET_ACTIVITY, \
    GET_CATEGORY_BY_ACTIVITY


def register_callbacks(app):
    @app.callback(
        Output('activity-dropdown', 'options'),
        Input('initial-load', 'data')  # Dispara o carregamento ao inicializar
    )
    def load_regions(_):
        db = Database()
        db.connect()
        activities = db.fetch_data(GET_ACTIVITY)
        db.close()

        # Convertendo os resultados para o formato de opções do Dash
        region_options = [{'label': activity[0], 'value': activity[0]} for activity in activities]
        return region_options

    @app.callback(
        Output('region-dropdown', 'options'),
        Input('initial-load', 'data')  # Dispara o carregamento ao inicializar
    )
    def load_regions(_):
        db = Database()
        db.connect()
        regions = db.fetch_data(GET_REGIONS)
        db.close()

        # Convertendo os resultados para o formato de opções do Dash
        region_options = [{'label': region[0], 'value': region[1]} for region in regions]
        return region_options

    @app.callback(
        Output('state-dropdown', 'options'),
        [
            Input('region-dropdown', 'value'),
         ]
    )
    def load_states(region):
        """Popula o dropdown de estados com dados do banco de dados."""
        db = Database()
        db.connect()
        states = db.fetch_data(GET_STATES, (region,))
        db.close()

        # Convertendo os resultados para o formato de opções do Dash
        state_options = [{'label': state[0], 'value': state[1]} for state in states]
        return state_options

    @app.callback(
        Output('city-dropdown', 'options'),
        Input('state-dropdown', 'value')
    )
    def load_cities(state):
        """Popula o dropdown de estados com dados do banco de dados."""
        db = Database()
        db.connect()
        cities = db.fetch_data(GET_CITIES, (state,))
        db.close()

        # Convertendo os resultados para o formato de opções do Dash
        city_options = [{'label': city[0], 'value': city[1]} for city in cities]
        return city_options

    @app.callback(
        Output('category-dropdown', 'options'),
        Input('activity-dropdown', 'value')
    )
    def load_categories(activity):
        db = Database()
        db.connect()
        categories = db.fetch_data(GET_CATEGORY_BY_ACTIVITY, (activity,))
        db.close()

        # Convertendo os resultados para o formato de opções do Dash
        category_options = [{'label': category[0], 'value': category[0]} for category in categories]
        return category_options

