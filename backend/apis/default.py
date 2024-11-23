from flask_restx import Resource, Namespace
from flask import make_response, jsonify, request
from datetime import datetime

ns_defaults = Namespace("Defaults endpoints", description="Operações para controlar processos gerais do sistema")


@ns_defaults.route('/years', strict_slashes=False)
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
