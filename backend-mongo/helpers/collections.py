from config.global_vars import IGNORE_Collections
from database.connection import db


def get_all_collections():
    collections = db.list_collection_names()  # Listar as coleções do banco de dados
    # Filtra as coleções removendo as que estão na lista 'collections_to_remove'
    collections_filtered = [col for col in collections if col not in IGNORE_Collections]
    collections_sorted = sorted(collections_filtered)
    return collections_sorted
