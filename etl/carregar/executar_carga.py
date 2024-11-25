import pymongo
import pandas as pd
import os
import yaml
import logging

with open("xpaths.yaml", "r") as file:
    xpaths = yaml.safe_load(file)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("carga.log"), logging.StreamHandler()],
)
logger = logging.getLogger()

# Dicionário para mapear os meses em português para números
mes_map = {
    "JAN": "01", "FEV": "02", "MAR": "03", "ABR": "04", "MAI": "05", "JUN": "06",
    "JUL": "07", "AGO": "08", "SET": "09", "OUT": "10", "NOV": "11", "DEZ": "12"
}

# Dicionário inverso para mapear números para meses em português
mes_map_inverso = {v: k for k, v in mes_map.items()}

def executar_carga(producao):
    """Realiza a carga incremental ou completa no MongoDB."""
    # Conexão com o MongoDB
    mongo_uri = os.getenv("MONGO_URI", "mongodb://sisab_database:27027")
    db_name = os.getenv("MONGO_DB", "sisab_v2")
    collection_name = xpaths[producao]["collection"]

    # Conecta ao banco e obtém a collection
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Caminho do arquivo transformado
    final_dir = os.getenv("FINAL_DIR", "data/consolidado")
    nome_arq = xpaths[producao]["nome_arq"]
    csv_path = os.path.join(final_dir, f"{nome_arq}.csv")

    if not os.path.exists(csv_path):
        logger.error(f"Arquivo transformado não encontrado para o tipo: {producao}")
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
        if "Ano" not in df.columns or "Mes" not in df.columns:
            logger.error("Colunas 'Ano' ou 'Mes' não encontradas no dataset. Verifique o formato do arquivo.")
            return

        # Converte a coluna 'mes' para números
        df["mes_num"] = df["Mes"].map(mes_map)

        # Ordena o DataFrame por ano e mês
        df = df.sort_values(by=["Ano", "mes_num"])

        # Identifica os últimos 3 meses no dataset
        ultimos_3_meses = df.drop_duplicates(subset=["Ano", "mes_num"], keep="last").tail(3)
        logger.info(f"Últimos 3 meses no dataset: {ultimos_3_meses[['Ano', 'Mes']].values.tolist()}")

        # Remove dados existentes no banco para os últimos 3 meses
        delete_conditions = []
        for _, row in ultimos_3_meses.iterrows():
            delete_conditions.append({"Ano": row["Ano"], "Mes": mes_map_inverso[row["mes_num"]]})

        result = collection.delete_many({"$or": delete_conditions})
        logger.info(f"{result.deleted_count} registros removidos da collection '{collection_name}'.")

        # Insere os novos dados
        data_to_insert = df.to_dict(orient="records")
        if data_to_insert:
            collection.insert_many(data_to_insert)
            logger.info(f"Novos dados inseridos com sucesso na collection '{collection_name}'.")

    # Fecha a conexão com o MongoDB
    client.close()