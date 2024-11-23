from flask import render_template, request, redirect, url_for, flash, make_response
from flask_restx import Resource

from database.collections import create_mongo_collection
from helpers.collections import  get_all_collections


class CreateCollection(Resource):

    def get(self):
        """
        :return: The method retrieves all collections from the database and renders the 'create_collection.html' template
                  with the collections list passed to it. Sets the 'Content-Type' response header to 'text/html'.
        """
        collections = get_all_collections()  # Listar as coleções do banco de dados
        response = make_response(render_template('create_collection.html', collections=collections))
        response.headers['Content-Type'] = 'text/html'
        return response

    def post(self):
        """
        Creates a new collection in the database and renders the 'create_collection.html' template
        """
        try:
            # Obtém o nome da coleção a partir do formulário
            collection_name = request.form['collection_name']

            # Verifica se a coleção existe ou a cria
            sucesso, mensagem = create_mongo_collection(collection_name)

            if sucesso:
                flash(mensagem, 'success')
            else:
                flash(mensagem, 'danger')
            collections = get_all_collections()  # Listar as coleções do banco de dados

            response = make_response(render_template('create_collection.html', collections=collections))
            response.headers['Content-Type'] = 'text/html'
            return response

            # return render_template('create_collection.html')

        except Exception as e:
            flash(f'Erro ao criar a coleção: {str(e)}', 'danger')
            return redirect(url_for('create_collection'))

