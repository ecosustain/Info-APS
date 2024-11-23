from flask_restx import Resource, Namespace
from flask import make_response, jsonify

from database.cities import get_cities_by_state

ns_cidades = Namespace("Cidades", description="Operações sobre os atributos dos municípios")


@ns_cidades.route("/cities/<state>", strict_slashes=False)
class City(Resource):
    def get(self, state):
        """
        Restorna todas as cidades de um Estado
        :param state: A sigla do estado
        :return: Retorna a coleção (Array) de todas as cidades do Estado
        """
        try:
            cities = get_cities_by_state(state)
            if cities:
                return jsonify(cities)
            else:
                return make_response(jsonify({"error": "UF não encontrada ou sem municípios associados"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
