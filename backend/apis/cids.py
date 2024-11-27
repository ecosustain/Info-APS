from database.collections import get_collection_attributes
from flask import jsonify, make_response
from flask_restx import Namespace, Resource
from helpers.aggregation import aggregation_by

ns_cids = Namespace("CIDS", description="Operações relacionadas a cids")


def agregacao_por_cid(collection, rows):
    collection_attributes = get_collection_attributes(collection)
    data = {}

    no_count = [
        "CIAP (N01) Cefaléia",
        "CIAP (R05) Tosse",
        "Ano",
        "Mes",
        "Uf",
        "Ibge",
        "Municipio",
    ]

    for row in rows:
        year, month = row["_id"]["Ano"], row["_id"]["Mes"]
        cid_total = sum(
            int(row[attribute])
            for attribute in collection_attributes
            if attribute not in no_count
        )

        data_year = data.get(year, {})
        data_year[month] = data_year.get(month, 0) + cid_total
        data[year] = data_year

    return data


@ns_cids.route("/cids_febre", strict_slashes=False)
class Cids(Resource):
    def get(self):
        """
        Soma os atributos que possuem Febre no nome da coleção CIDS de todos os dados
        :return: Resposta JSON com coleções para a região e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro desconhecido
        """
        try:
            collection = "CIDS"
            rows = aggregation_by(collection, ["Ano", "Mes"])
            data = agregacao_por_cid(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_cids.route("/cids_febre/regions/<region>", strict_slashes=False)
class CidsPorRegiao(Resource):
    def get(self, region):
        """
        Soma os atributos que possuem Febre no nome da coleção CIDS
        :param region: Código da região utilizada para realizar a busca
        :return: Resposta JSON com coleções para a região e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro desconhecido
        """
        try:
            collection = "CIDS"
            rows = aggregation_by(collection, ["Ano", "Mes"], [int(region)])
            data = agregacao_por_cid(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_cids.route("/cids_febre/states/<state>", strict_slashes=False)
class CidsPorEstado(Resource):
    def get(self, state):
        """
        Soma os atributos possuiem Febre no nome da coleção CIDS
        :param region: O estado para o qual os cids hospitalares serão recuperados
        :return: Resposta JSON com as coleções para o estado e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro
        """
        try:
            collection = "CIDS"
            rows = aggregation_by(collection, ["Ano", "Mes"], None, [state])
            data = agregacao_por_cid(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_cids.route("/cids_febre/cities/<ibge>", strict_slashes=False)
class CidsPorCidade(Resource):
    def get(self, ibge):
        """
        Soma os atributos possuiem Febre no nome da coleção CIDS para uma cidade específica

        :param region: Código IBGE da cidade para a qual deseja realizar a soma dos cids
        :return: Resposta JSON com as coleções para o estado e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro
        """
        try:
            collection = "CIDS"
            rows = aggregation_by(
                collection, ["Ano", "Mes"], None, None, [int(ibge)]
            )
            data = agregacao_por_cid(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
