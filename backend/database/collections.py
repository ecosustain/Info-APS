from .connection import db


def create_mongo_collection(collection_name):
    collections = db.list_collection_names()

    if collection_name in collections:
        return (
            False,
            f"A coleção '{collection_name}' já existe no banco de dados.",
        )

    db.create_collection(collection_name)
    return True, f"A coleção '{collection_name}' foi criada com sucesso."


def get_collection_sum_X(collection_name, ignore_keys=None, IGNORE_KEYS=None):
    collection = db[collection_name]
    ignore_keys = ignore_keys or IGNORE_KEYS

    documents = collection.find()
    collection_summary = {}

    for document in documents:
        for key, value in document.items():
            if key not in ignore_keys and isinstance(value, (int, float)):
                collection_summary[key] = (
                    collection_summary.get(key, 0) + value
                )
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        key_composta = f"{key}.{sub_key}"
                        collection_summary[key_composta] = (
                            collection_summary.get(key_composta, 0) + sub_value
                        )
    return collection_summary


def get_collection_attributes(collection_name):
    # Consultar a coleção 'collection_attributes' para encontrar os atributos da coleção especificada
    result = db["collection_attributes"].find_one(
        {"collection": collection_name},  # Filtro pelo nome da coleção
        {
            "_id": 0,
            "attributes": 1,
        },  # Excluir o campo '_id', retornar apenas os atributos
    )

    if result:
        return result["attributes"]
    else:
        return []


def get_collection_count(collection_name):
    collection = db[collection_name]
    count = collection.count_documents({})
    return count
