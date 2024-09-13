# callbacks/update_tables.py

from dash.dependencies import Input, Output
from data.database import Database
from utils.queries import GET_STATES, GET_REGIONS, GET_CITIES, GET_CATEGORY_BY_CITY, GET_CATEGORY_ALL, GET_ACTIVITY, \
    GET_CATEGORY_BY_ACTIVITY, GET_ALL_YEAR


def register_callbacks(app):
    @app.callback(
        Output('year-dropdown-map', 'options'),
        Input('initial-load-map', 'data')  # Dispara o carregamento ao inicializar
    )
    def load_regions(_):
        db = Database()
        db.connect()
        years = db.fetch_data(GET_ALL_YEAR)
        db.close()

        # Convertendo os resultados para o formato de opções do Dash
        region_options = [{'label': year[0], 'value': year[0]} for year in years]
        return region_options
    @app.callback(
        Output('activity-dropdown-map', 'options'),
        Input('initial-load-map', 'data')  # Dispara o carregamento ao inicializar
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
        Output('category-dropdown-map', 'options'),
        Input('activity-dropdown-map', 'value')
    )
    def load_categories(activity):
        db = Database()
        db.connect()
        categories = db.fetch_data(GET_CATEGORY_BY_ACTIVITY, (activity,))
        db.close()

        # Convertendo os resultados para o formato de opções do Dash
        category_options = [{'label': category[0], 'value': category[0]} for category in categories]
        return category_options

