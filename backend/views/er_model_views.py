from flask_restx import Resource
from flask import render_template, request, redirect, url_for, flash, make_response

class ErModelView(Resource):

    def get(self):
        """
        :return: The method retrieves all collections from the database and renders the 'create_collection.html' template
                  with the collections list passed to it. Sets the 'Content-Type' response header to 'text/html'.
        """
        response = make_response(render_template('er_model.html'))
        response.headers['Content-Type'] = 'text/html'
        return response