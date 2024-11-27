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

# Conexão com o MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://sisab_database:27017")
db_name = os.getenv("MONGO_DB", "sisab_v2")

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


def get_cities():
    """Extrair dados únicos da coleção População"""
    # Conecta ao banco e obtém a collection
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    populacao_collection = db['População']
    pipeline = [
        {
            "$group": {
                "_id": "$Ibge",
                "uf": {"$first": "$Uf"},
                "cidade": {"$first": "$Municipio"}
            }
        }
    ]
    populacao_dados = list(populacao_collection.aggregate(pipeline))

    # Transformar os dados para o formato desejado
    cities_dados = [
        {
            "_id": dado["_id"],
            "uf": dado["uf"],
            "cidade": dado["cidade"]
        }
        for dado in populacao_dados
    ]
    client.close()
    return cities_dados


def get_states():
    """Dados dos estados brasileiros."""
    uf_data = [
        {"name": "AC", "description": "Acre"},
        {"name": "AL", "description": "Alagoas"},
        {"name": "AM", "description": "Amazonas"},
        {"name": "AP", "description": "Amapá"},
        {"name": "BA", "description": "Bahia"},
        {"name": "CE", "description": "Ceará"},
        {"name": "DF", "description": "Distrito Federal"},
        {"name": "ES", "description": "Espírito Santo"},
        {"name": "GO", "description": "Goiás"},
        {"name": "MA", "description": "Maranhão"},
        {"name": "MG", "description": "Minas Gerais"},
        {"name": "MS", "description": "Mato Grosso do Sul"},
        {"name": "MT", "description": "Mato Grosso"},
        {"name": "PA", "description": "Pará"},
        {"name": "PB", "description": "Paraíba"},
        {"name": "PE", "description": "Pernambuco"},
        {"name": "PI", "description": "Piauí"},
        {"name": "PR", "description": "Paraná"},
        {"name": "RJ", "description": "Rio de Janeiro"},
        {"name": "RN", "description": "Rio Grande do Norte"},
        {"name": "RO", "description": "Rondônia"},
        {"name": "RR", "description": "Roraima"},
        {"name": "RS", "description": "Rio Grande do Sul"},
        {"name": "SC", "description": "Santa Catarina"},
        {"name": "SE", "description": "Sergipe"},
        {"name": "SP", "description": "São Paulo"},
        {"name": "TO", "description": "Tocantins"}
    ]

    return uf_data


def popular_tabelas_especificas():
    """Popula tabelas específicas como UF e Cidades."""
    # Conecta ao banco e obtém a collection
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    uf_collection = db["states"]
    # Popula a tabela de UF
    uf_collection.insert_many(get_states())
    # Popula a tabela de Cidades
    cidades_collection = db.get_collection("cities")
    cidades_data = get_cities()
    cidades_collection.insert_many(cidades_data)

    client.close()


IGNORE_Collections = ["collection_attributes", "states", "cities"]

def get_all_collections():
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    collections = db.list_collection_names()  # Listar as coleções do banco de dados
    # Filtra as coleções removendo as que estão na lista 'collections_to_remove'
    collections_filtered = [col for col in collections if col not in IGNORE_Collections]
    collections_sorted = sorted(collections_filtered)
    client.close()
    return collections_sorted


def update_collection_attributes(collection_name, based_on_first=None):
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    # Obter a coleção onde os documentos estão
    collection = db[collection_name]
    if based_on_first:
        documents = [collection.find_one()]
    else:
        documents = collection.find()

    # Usar um set para evitar duplicatas
    attributes_set = set()

    # Iterar sobre todos os documentos da coleção e coletar os atributos (chaves)
    for document in documents:
        for key in document.keys():
            # Adicionar o atributo à lista de atributos
            if key != "_id":  # Ignorar o campo '_id'
                attributes_set.add(key)

    # Converter o set para uma lista ordenada
    attributes_list = sorted(list(attributes_set))

    # Inserir ou atualizar os atributos na coleção 'collection_attributes'
    db['collection_attributes'].update_one(
        {'collection': collection_name},  # Filtro para a coleção específica
        {'$set': {'attributes': attributes_list}},  # Atualização da lista de atributos
        upsert=True  # Insere um novo documento se não encontrar a coleção
    )
    client.close()
    return attributes_list


def update_collections_attributes(collection_name=None, based_on_first=None):
    if collection_name:
        print(collection_name)
        attributes_list = update_collection_attributes(collection_name, based_on_first)
        print(attributes_list)
    else:
        collections = get_all_collections()
        for collection_name in collections:
            print(collection_name)
            attributes_list = update_collection_attributes(collection_name, based_on_first)
            print(attributes_list)


def remove_dots_from_keys():
    """Função para remover pontos dos nomes das colunas nas coleções do MongoDB"""
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]

    # Iterar sobre todas as coleções no banco de dados
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        for document in collection.find():
            updated_document = {}
            needs_update = False

            # Verificar e renomear as chaves que contêm pontos
            for key, value in document.items():
                if '.' in key:
                    new_key = key.replace('.', '_')
                    updated_document[new_key] = value
                    needs_update = True
                else:
                    updated_document[key] = value

            # Atualizar o documento se necessário
            if needs_update:
                collection.update_one({'_id': document['_id']}, {'$set': updated_document, '$unset': {key: "" for key in document if '.' in key}})

    print("Remoção de pontos das chaves concluída.")