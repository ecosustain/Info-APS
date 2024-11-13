from flask import (flash, make_response, redirect, render_template, request,
                   url_for)
from flask_restx import Resource


class ErModelView(Resource):

    def get(self):
        """
        :return: The method retrieves all collections from the database and renders the 'create_collection.html' template
                  with the collections list passed to it. Sets the 'Content-Type' response header to 'text/html'.
        """
        response = make_response(render_template("er_model.html"))
        response.headers["Content-Type"] = "text/html"
        return response
