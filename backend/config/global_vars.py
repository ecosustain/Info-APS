import os

IGNORE_KEYS = [
    "Uf",
    "Ibge",
    "Municipio",
    "Mes",
    "Ano",
    "latitude",
    "longitude",
    "region",
    "region_name",
    "city_id",
    "region_id",
]

IGNORE_Collections = [
    "states",
    "cities",
    "collection_attributes",
    "years",
    "data_import_profile",
    "regions",
    "shapefiles",
]
# API_SERVER = "http://127.0.0.1:5000/api/v1"
API_SERVER = os.getenv("API_SERVER", "http://localhost:5000/api/v1")
