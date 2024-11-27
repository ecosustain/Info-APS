from config.global_vars import API_SERVER
from flask import make_response, render_template
from flask_restx import Resource
from helpers.collections import get_all_collections


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
