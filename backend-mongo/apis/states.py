from database.states import (
    get_collection_sum_states,
    get_collection_sum_states_year,
    get_state,
)
from flask import jsonify, make_response
from flask_restx import Namespace, Resource

ns_estados = Namespace(
    "Estados", description="Operações sobre os atributos dos estados"
)


@ns_estados.route("/states", strict_slashes=False)
class State(Resource):
    def get(self):
        """
        Consulta os estados brasileiros
        :return: Retorna a lista de estados brasileiros
        """
        try:
            states = get_state()
            return make_response(jsonify(states), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_estados.route("/states/<state>/sum", strict_slashes=False)
class StateSumByCollection(Resource):

    def get(self, state):
        """
        Soma todos os atributos de todas as coleções por estado
        :param state: A sigla do estado
        :return: Uma lista por para cada estado com: Todos os atributos somados de todas as coleções enviadas até o momento para o estado.
        """
        try:
            collections = get_collection_sum_states([state])
            if collections:
                return jsonify(collections)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_estados.route("/states/<state>/<year>/sum", strict_slashes=False)
class StateSumByCollectionYear(Resource):

    def get(self, state, year):
        """
        Soma todos os atributos de todas as coleções por estado e ano
        :param state: A sigla do estado e ano
        :return: Uma lista por para cada estado com: Todos os atributos somados de todas as coleções enviadas para o estado e ano.
        """
        try:
            collections = get_collection_sum_states_year([state], int(year))
            if collections:
                return jsonify(collections)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
