# callbacks/update_map_graph.py
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
from data.database import Database
from utils.queries import GET_MAP_REGION_DATA, GET_MAP_STATE_DATA, GET_MAP_CITY_DATA, GET_MAP_REGION_DATA_INIT, \
    GET_MAP_CATEGORY_DATA, GET_MAP_ALL_CATEGORY_DATA
from sklearn.preprocessing import MinMaxScaler

def is_valid(value):
    """Checks if a value is not None and not an empty list"""
    return not (value is None or (isinstance(value, list) and len(value) == 0))

def register_callbacks(app):

    @app.callback(
        Output('map', 'figure', allow_duplicate=True),
        [
            Input('activity-dropdown-map', 'value'),
            Input('category-dropdown-map', 'value'),
            Input('year-dropdown-map', 'value'),
         ]
    )
    def update_map_graph(activity, category, year):
        db = Database()
        db.connect()

        is_category = is_valid(category)
        is_activity = is_valid(activity)
        is_year = is_valid(year)
        zoom = 3.5

        data = None

        if  is_activity:
            if not is_category:
                category = None
            if not is_year:
                year = None

            data = db.fetch_data(GET_MAP_CATEGORY_DATA, (activity, category,category, year, year))


        db.close()


        return update_image_map(data, zoom)

    def update_image_map(data, zoom):

        if data:
            df = pd.DataFrame(data, columns=['name', 'latitude', 'longitude', 'total', 'parent_id', 'geo_unit'])
        else:
            df = pd.DataFrame(columns=['name', 'latitude', 'longitude', 'total', 'parent_id', 'geo_unit'])


        fig = px.scatter_map(df, lat="latitude", lon="longitude", color="name", size="total", hover_data=["name", "geo_unit", "total"],
                             color_discrete_sequence=px.colors.sequential.Jet,
                             zoom=zoom,
                             )
        fig.update_layout(map_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig