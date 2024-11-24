import pymongo
import pandas as pd
import os

def executar_carga(tipo):
    """Realiza a carga incremental ou completa no MongoDB."""
    # Conexão com o MongoDB
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB", "etl_database")
    collection_name = f"{tipo}_collection"

    # Conecta ao banco e obtém a collection
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Caminho do arquivo transformado
    transform_dir = os.getenv("TRANSFORM_DIR", "data/transformacao")
    csv_path = os.path.join(transform_dir, f"{tipo}.csv")

    if not os.path.exists(csv_path):
        logger.error(f"Arquivo transformado não encontrado para o tipo: {tipo}")
        return

    # Lê o arquivo CSV transformado
    logger.info(f"Lendo dados transformados de {csv_path}...")
    df = pd.read_csv(csv_path)

    # Verifica se a collection já existe no banco
    if collection_name not in db.list_collection_names():
        logger.info(f"Collection '{collection_name}' não existe. Realizando carga completa...")
        # Carga completa
        data_to_insert = df.to_dict(orient="records")
        if data_to_insert:
            collection.insert_many(data_to_insert)
            logger.info(f"Dados inseridos com sucesso na collection '{collection_name}'.")
    else:
        logger.info(f"Collection '{collection_name}' encontrada. Realizando carga incremental...")
        # Identifica a menor data no dataset
        if "data" not in df.columns:
            logger.error("Coluna 'data' não encontrada no dataset. Verifique o formato do arquivo.")
            return

        df["data"] = pd.to_datetime(df["data"])  # Converte a coluna para datetime
        min_date = df["data"].min()

        logger.info(f"Menor data no dataset: {min_date}")

        # Remove dados existentes no banco com data >= menor data do novo dataset
        result = collection.delete_many({"data": {"$gte": min_date}})
        logger.info(f"{result.deleted_count} registros removidos da collection '{collection_name}'.")

        # Insere os novos dados
        data_to_insert = df.to_dict(orient="records")
        if data_to_insert:
            collection.insert_many(data_to_insert)
            logger.info(f"Novos dados inseridos com sucesso na collection '{collection_name}'.")

    # Fecha a conexão com o MongoDB
    client.close()
