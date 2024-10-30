from flask_restx import Resource, Namespace
from flask import make_response, jsonify

from database.collections import get_collection_attributes
from helpers.aggregation import aggregation_by

ns_encaminhamentos = Namespace(
    "Encaminhamentos", description="Operações relacionadas a encaminhamentos"
)


def agregacao_por_encaminhamento(collection, rows):
    collection_attributes = get_collection_attributes(collection)
    data = {}

    for row in rows:
        year, month = row["_id"]["Ano"], row["_id"]["Mes"]
        encaminhamento_total = sum(
            int(row[attribute])
            for attribute in collection_attributes
            if "Encaminhamento" in attribute
        )

        data_year = data.get(year, {})
        data_year[month] = data_year.get(month, 0) + encaminhamento_total
        data[year] = data_year

    return data


@ns_encaminhamentos.route("/encaminhamentos", strict_slashes=False)
class EncaminhamentosHospitalar(Resource):
    def get(self):
        """
        Soma os atributos que possuem Encaminhamento no nome da coleção Produção Conduta de todos os dados
        :return: Resposta JSON com coleções para a região e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro desconhecido
        """
        try:
            collection = "Produção Conduta"
            rows = aggregation_by(collection, ["Ano", "Mes"])
            data = agregacao_por_encaminhamento(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_encaminhamentos.route(
    "/encaminhamentos/regions/<region>", strict_slashes=False
)
class EncaminhamentosHospitalarPorRegiao(Resource):
    def get(self, region):
        """
        Soma os atributos que possuem Encaminhamento no nome da coleção Produção Conduta
        :param region: Código da região utilizada para realizar a busca
        :return: Resposta JSON com coleções para a região e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro desconhecido
        """
        try:
            collection = "Produção Conduta"
            rows = aggregation_by(collection, ["Ano", "Mes"], [int(region)])
            data = agregacao_por_encaminhamento(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_encaminhamentos.route(
    "/encaminhamentos/states/<state>", strict_slashes=False
)
class EncaminhamentosHospitalarPorEstado(Resource):
    def get(self, state):
        """
        Soma os atributos possuiem Encaminhamento no nome da coleção Produção Conduta
        :param region: O estado para o qual os encaminhamentos hospitalares serão recuperados
        :return: Resposta JSON com as coleções para o estado e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro
        """
        try:
            collection = "Produção Conduta"
            rows = aggregation_by(collection, ["Ano", "Mes"], None, [state])
            data = agregacao_por_encaminhamento(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_encaminhamentos.route(
    "/encaminhamentos/cities/<ibge>", strict_slashes=False
)
class EncaminhamentosHospitalarPorCidade(Resource):
    def get(self, ibge):
        """
        Soma os atributos possuiem Encaminhamento no nome da coleção Produção Conduta para uma cidade específica

        :param region: Código IBGE da cidade para a qual deseja realizar a soma dos encaminhamentos
        :return: Resposta JSON com as coleções para o estado e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro
        """
        try:
            collection = "Produção Conduta"
            rows = aggregation_by(
                collection, ["Ano", "Mes"], None, None, [int(ibge)]
            )
            data = agregacao_por_encaminhamento(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
