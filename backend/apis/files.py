import os
import tempfile
import zipfile

import pandas as pd
from database.collections import get_collection_attributes
from database.connection import db
from flask import jsonify, make_response, request, send_file
from flask_restx import Namespace, Resource
from helpers.progress_bar import ProgressManager
from helpers.utils import (  # Importando funções utilitárias
    is_collection_empty,
    process_csv_file,
    update_collections_attributes,
)

ns_files = Namespace(
    "Sistema e Arquivos",
    description="Operações de apoio a operação do sistema",
)


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


@ns_files.route("/files/download_data", strict_slashes=False, methods=["POST"])
class FileDownload(Resource):
    def get(self):
        return make_response(jsonify({"files": os.listdir(os.getcwd())}), 200)

    def post(self):
        """
        Faz o download de uma coleção no formato csv, json ou parquet.
        :return: Retorna o arquivo comprimido em zip.
        """
        # Extrair os parâmetros da requisição
        collection_name = request.json.get("collection_name")
        progress_id = request.json.get("progress_id")
        years = request.json.get("years", [])
        state = request.json.get("state", "")
        cities = request.json.get("cities", [])
        attributes = request.json.get("attributes", [])
        file_format = request.json.get("format", "csv")
        total_records = 4
        step = 0

        progress_manager = ProgressManager()

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
            cities = [
                int(city) for city in cities
            ]  # Converte cada elemento de cities para inteiro
            query["Ibge"] = {
                "$in": cities
            }  # Se a lista de municípios não estiver vazia

        step += 1
        progress_manager.set_progress(
            progress_id,
            int((step / total_records) * 100),
            f"{step}/{total_records}",
        )
        try:
            # Executar a consulta no MongoDB
            documents = list(collection.find(query))

            # Se nenhum documento foi encontrado, retornar um erro
            if not documents:
                message = "Nenhum dado encontrado para os filtros fornecidos"
                progress_manager.set_progress(progress_id, 100, message)
                return make_response(jsonify({"error": message}), 404)

            # Filtrar os atributos desejados (se a lista de atributos estiver vazia, selecionar todos)
            if not attributes:
                # Se nenhum atributo foi fornecido, incluir todos os atributos de todos os documentos
                attributes = get_collection_attributes(collection_name)
            else:
                # Manter somente os atributos selecionados
                collection_attributes = get_collection_attributes(
                    collection_name
                )
                attributes = [
                    attr
                    for attr in attributes
                    if attr in collection_attributes
                ]

            step += 1
            progress_manager.set_progress(
                progress_id,
                int((step / total_records) * 100),
                f"{step}/{total_records}",
            )

            # Converter os documentos filtrados para DataFrame
            df = pd.DataFrame(documents)

            # Selecionar somente as colunas que são atributos presentes nos documentos
            selected_columns = [col for col in attributes if col in df.columns]
            df = df[selected_columns]

            step += 1
            progress_manager.set_progress(
                progress_id,
                int((step / total_records) * 100),
                f"{step}/{total_records}",
            )

            # Geração de um nome de arquivo aleatório e temporário
            with tempfile.TemporaryDirectory() as tmpdirname:
                # Nome do arquivo exportado (antes de compactar)
                file_path = os.path.join(
                    tmpdirname, f"{collection_name}.{file_format}"
                )
                zip_path = os.path.join(tmpdirname, f"{collection_name}.zip")
                export_data(df, file_format, file_path, zip_path)

                step += 1
                progress_manager.set_progress(
                    progress_id,
                    int((step / total_records) * 100),
                    f"{step}/{total_records}",
                )

                return send_file(
                    zip_path,
                    as_attachment=True,
                    download_name=f"{collection_name}.zip",
                    mimetype="application/zip",
                )

            # progress_manager.set_progress(progress_id, 100, "Não foi possível enviar o arquivo")
            # return make_response(jsonify({"Não foi possível enviar o arquivo"}), 500)
        except Exception as e:
            message = f"Erro ao processar o arquivo: {str(e)}"
            progress_manager.set_progress(progress_id, 100, message)
            return make_response(jsonify({"message": message}), 400)


@ns_files.route("/files/upload_data", strict_slashes=False, methods=["POST"])
class UploadFile(Resource):
    def post(self):
        """
        Envia e processa um arquivo CSV com dados de uma coleção.

        :return: Uma resposta JSON com uma mensagem de sucesso ou erro e um código de status HTTP.
        """
        try:
            progress_manager = ProgressManager()

            # Obter o arquivo CSV enviado
            file = request.files["file"]
            progress_id = request.form["progress_id"]
            collection_name = request.form["collection"]
            has_no_attributes = is_collection_empty(collection_name)
            if file and file.filename.endswith(".csv"):
                # Processar o CSV e inserir os dados no MongoDB
                total_imported = process_csv_file(
                    file, collection_name, progress_id
                )
                message = f"Arquivo {file.filename} enviado e processado com sucesso. Total de registros: {total_imported}"
                return make_response(jsonify({"message": message}), 200)

            else:
                message = "Por favor, faça o upload de um arquivo CSV válido."
                progress_manager.set_progress(progress_id, 100)
                return make_response(jsonify({"message": message}), 400)

        except Exception as e:
            message = f"Erro ao processar o arquivo: {str(e)}"
            progress_manager.set_progress(progress_id, 100, message)
            return make_response(jsonify({"message": message}), 400)

        finally:
            if has_no_attributes:
                # Atualiza os atributos da collection, pois essa éa primeira vez que esta sendo populada
                update_collections_attributes(collection_name, True)
