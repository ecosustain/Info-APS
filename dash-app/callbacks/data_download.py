import pandas as pd
from dash import  dcc, Input, Output, callback

from data.database import Database
from utils.queries import GET_DATA_BY_ACTIVITY, GET_DATA_BY_REGION_ALL, GET_DATA_BY_REGION, GET_DATA_BY_STATE, \
    GET_DATA_BY_CITY
from utils.validation import is_valid


def register_callbacks(app):

    @app.callback(
        Output("download-dataframe-csv", "data"),
        [
            Input("btn_csv", "n_clicks"),
            Input('region-dropdown', 'value'),
            Input('state-dropdown', 'value'),
            Input('city-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('activity-dropdown', 'value'),
         ], prevent_initial_call=True

    )

    def update_bar_graph(n_clicks, region, state, city, category, activity):

        db = Database()
        db.connect()
        data = None

        is_region = is_valid(region)
        is_state = is_valid(state)
        is_city = is_valid(city)
        is_category = is_valid(category)
        is_activity = is_valid(activity)

        if is_activity and n_clicks:
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
            if not is_region and n_clicks:
                data = db.fetch_data(GET_DATA_BY_REGION_ALL)

            if is_region and not is_state and not is_city and not is_category and n_clicks:
                data = db.fetch_data(GET_DATA_BY_REGION, (region,))

            if is_region and is_state and not is_city and not is_category and n_clicks:
                data = db.fetch_data(GET_DATA_BY_STATE, (state,))

            if is_region and is_state and is_city and not is_category and n_clicks:
                data = db.fetch_data(GET_DATA_BY_CITY, (city,))

        if data:
            df = pd.DataFrame(data, columns=['name', 'total', 'geo_unit', 'year'])
            return dcc.send_data_frame(df.to_csv, "saude_basica.csv")