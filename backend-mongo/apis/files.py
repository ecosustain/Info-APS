import os
import tempfile
import zipfile
from datetime import datetime

import pandas as pd
from database.collections import get_collection_attributes
from database.connection import db
from flask import jsonify, make_response, request, send_file
from flask_restx import Namespace, Resource

# Variável global para acompanhar o progresso
progress_bar = {
    "total": 0,  # Total de registros
    "processed": 0,  # Quantidade de registros processados
    "progress": 0,  # Progresso percentual
    "timestamp": 0,  # Progresso percentual
}

ns_default = Namespace(
    "Sistema e Arquivos",
    description="Operações de apoio a operação do sistema",
)


def get_progress():
    global progress_bar
    return progress_bar


def start_progress(total, processed, progress):
    global progress_bar
    progress_bar["total"] = total
    progress_bar["processed"] = processed
    progress_bar["progress"] = progress
    progress_bar["timestamp"] = datetime.now().timestamp()


def set_progress(processed, progress):
    global progress_bar
    progress_bar["processed"] = processed
    progress_bar["progress"] = progress
    progress_bar["timestamp"] = datetime.now().timestamp()


def reset_progress():
    global progress_bar
    progress_bar["total"] = 0
    progress_bar["processed"] = 0
    progress_bar["progress"] = 0
    progress_bar["timestamp"] = 0


@ns_default.route("/progress", strict_slashes=False)
class ProgressBarStatus(Resource):
    def get(self):
        """
        :return: states data as a response with HTTP status code 200 if successful, or an error message with HTTP status code 500
        """
        try:
            response = make_response(jsonify(get_progress()), 200)
            response.headers["Cache-Control"] = (
                "no-cache, no-store, must-revalidate"
            )
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_default.route("/progress_reset", strict_slashes=False)
class ProgressBarReset(Resource):
    def get(self):
        """
        :return: states data as a response with HTTP status code 200 if successful, or an error message with HTTP status code 500
        """
        try:
            reset_progress()
            response = make_response(jsonify(get_progress()), 200)
            response.headers["Cache-Control"] = (
                "no-cache, no-store, must-revalidate"
            )
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


def export_data(df, file_format, file_path, zip_path):
    chunk_size = 10000  # Define o tamanho do chunk para exportar (ajuste conforme necessário)

    # Exportar os dados para um arquivo no disco em chunks
    if file_format == "csv":
        # Criar o CSV diretamente no disco em chunks
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            # Exportar o DataFrame em chunks
            for i, chunk in enumerate(range(0, len(df), chunk_size)):
                df.iloc[chunk : chunk + chunk_size].to_csv(
                    file, index=False, header=i == 0
                )  # Cabeçalho apenas no primeiro chunk

    elif file_format == "parquet":
        # Criar o Parquet diretamente no disco em chunks
        df.to_parquet(file_path, index=False)

    elif file_format == "json":
        # Criar o JSON diretamente no disco
        df.to_json(file_path, orient="records", lines=False)

    else:
        return jsonify({"error": "Formato de exportação não suportado"}), 400

    # Zipar o arquivo criado
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(file_path, os.path.basename(file_path))

    # Enviar o arquivo zipado como resposta
    return zip_path


@ns_default.route(
    "/files/download_data", strict_slashes=False, methods=["POST"]
)
class Files(Resource):
    def get(self):
        return make_response(jsonify({"files": os.listdir(os.getcwd())}), 200)

    def post(self):
        # Extrair os parâmetros da requisição
        collection_name = request.json.get("collection_name")
        years = request.json.get("years", [])
        state = request.json.get("state", "")
        cities = request.json.get("cities", [])
        attributes = request.json.get("attributes", [])
        file_format = request.json.get("format", "csv")
        total_records = 4
        step = 0

        start_progress(total_records, 0, 0)

        # Conectar à coleção do MongoDB
        collection = db[collection_name]

        # Criar a consulta para o MongoDB
        query = {}

        # Filtro para Anos
        if years:
            years = list(map(int, years))  # converts all
            query["Ano"] = {
                "$in": years
            }  # Se a lista de anos não estiver vazia
        # Filtro para Estado
        if state:
            query["Uf"] = state  # Se o estado for fornecido
        # Filtro para Municípios
        if cities:
            query["Municipio"] = {
                "$in": cities
            }  # Se a lista de municípios não estiver vazia

        set_progress(step + 1, int(((step + 1) / total_records) * 100))
        step += 1

        # Executar a consulta no MongoDB
        documents = list(collection.find(query))

        # Se nenhum documento foi encontrado, retornar um erro
        if not documents:
            set_progress(total_records, 100)

            return make_response(
                jsonify(
                    {
                        "error": "Nenhum dado encontrado para os filtros fornecidos"
                    }
                ),
                404,
            )

        # Filtrar os atributos desejados (se a lista de atributos estiver vazia, selecionar todos)
        if not attributes:
            # Se nenhum atributo foi fornecido, incluir todos os atributos de todos os documentos
            # attributes = list(documents[0].keys())  # Usar os atributos do primeiro documento
            # attributes.remove('_id')  # Remover o campo '_id'
            attributes = get_collection_attributes(collection_name)
        else:
            # Manter somente os atributos selecionados
            collection_attributes = get_collection_attributes(collection_name)
            attributes = [
                attr for attr in attributes if attr in collection_attributes
            ]

        set_progress(step + 1, int(((step + 1) / total_records) * 100))
        step += 1

        # Converter os documentos filtrados para DataFrame
        df = pd.DataFrame(documents)

        # Manter somente as colunas selecionadas (atributos)
        df = df[attributes]

        set_progress(step + 1, int(((step + 1) / total_records) * 100))
        step += 1

        # Geração de um nome de arquivo aleatório e temporário
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Nome do arquivo exportado (antes de compactar)
            file_path = os.path.join(
                tmpdirname, f"{collection_name}.{file_format}"
            )
            zip_path = os.path.join(tmpdirname, f"{collection_name}.zip")
            export_data(df, file_format, file_path, zip_path)

            set_progress(step + 1, int(((step + 1) / total_records) * 100))
            step += 1

            return send_file(
                zip_path,
                as_attachment=True,
                download_name=f"{collection_name}.zip",
                mimetype="application/zip",
            )

        return make_response(
            jsonify({"Não foi possível enviar o arquivo"}), 500
        )


@ns_default.route("/years", strict_slashes=False)
class YearInterval(Resource):
    def get(self):
        """
        Lista todos os anos cadastrado no sistema
        :return: Retorna a lista de anos encontradas no sistema.
        """
        try:
            current_year = datetime.now().year
            years = list(range(2013, current_year + 1))
            return jsonify(years)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
