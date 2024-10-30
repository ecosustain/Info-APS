from apis.files import reset_progress
from config.global_vars import API_SERVER
from flask import flash, jsonify, make_response, render_template, request
from flask_restx import Resource
from helpers.collections import get_all_collections
from helpers.utils import (  # Importando funções utilitárias
    is_collection_empty,
    process_csv_file,
    update_collections_attributes,
)


class DownloadFile(Resource):
    def get(self):
        """
        :return: A Flask response object containing the rendered template 'download.html' with a list of all collections retrieved from the database.
        """
        collections = (
            get_all_collections()
        )  # Listar as coleções do banco de dados
        response = make_response(
            render_template(
                "download.html", collections=collections, api_server=API_SERVER
            )
        )
        response.headers["Content-Type"] = "text/html"
        return response

    def post(self):
        """
        Downloaded file with a list of all collections retrieved from the database.
        :return: sucess message and list of all collections retrieved from the database or error message with code 400.
        """
        try:
            # Obter o arquivo CSV enviado
            file = request.files["file"]
            collection_name = request.form["collection"]
            reset_progress()

            if file and file.filename.endswith(".csv"):
                # Processar o CSV e inserir os dados no MongoDB
                process_csv_file(file, collection_name)
                message = f"Arquivo {file.filename} enviado e processado com sucesso!"
                flash(message, "success")
                return jsonify({"message": message}), 200
            else:
                message = "Por favor, faça o upload de um arquivo CSV válido."
                flash(message, "danger")
                return jsonify({"message": message}), 400

        except Exception as e:
            message = f"Erro ao processar o arquivo: {str(e)}"
            flash(message, "danger")
            return jsonify({"message": message}), 400

        # finally:
        # progress_reset()
        # collections = get_all_collections()  # Listar as coleções do banco de dados
        # response = make_response(render_template('upload.html', collections=collections))
        # response.headers['Content-Type'] = 'text/html'
        # return response


class UploadCSV(Resource):
    def get(self):
        """
        :return: Return a response object with the 'upload.html' template rendered, containing a list of all collections in the database passed as 'collections'. The response headers are set with 'Content-Type' as 'text/html'.
        """
        collections = (
            get_all_collections()
        )  # Listar as coleções do banco de dados
        response = make_response(
            render_template(
                "upload.html", collections=collections, api_server=API_SERVER
            )
        )
        response.headers["Content-Type"] = "text/html"
        return response

    def post(self):
        """
        import sent data to collection
        :return: None
        """
        try:
            # Obter o arquivo CSV enviado
            file = request.files["file"]
            collection_name = request.form["collection"]
            reset_progress()
            has_no_attributes = is_collection_empty(collection_name)
            if file and file.filename.endswith(".csv"):
                # Processar o CSV e inserir os dados no MongoDB
                process_csv_file(file, collection_name)
                message = f"Arquivo {file.filename} enviado e processado com sucesso!"
                flash(message, "success")
                return jsonify({"message": message}), 200
            else:
                message = "Por favor, faça o upload de um arquivo CSV válido."
                flash(message, "danger")
                return jsonify({"message": message}), 400

        except Exception as e:
            message = f"Erro ao processar o arquivo: {str(e)}"
            flash(message, "danger")
            return jsonify({"message": message}), 400

        finally:
            if has_no_attributes:
                # Atualiza os atributos da collection, pois essa éa primeira vez que esta sendo populada
                update_collections_attributes(collection_name, True)
