from database.collections import get_collection_attributes
from flask import jsonify, make_response
from flask_restx import Namespace, Resource
from helpers.aggregation import aggregation_by

ns_altas = Namespace(
    "Altas",
    description="Operações sobre os atributos da coleção Produção Conduta",
)


def agregacao_por_altas(collection, rows):
    attributes = get_collection_attributes(collection)
    data = {}

    for row in rows:
        year_month = (row["_id"]["Ano"], row["_id"]["Mes"])
        highs_total = sum(
            int(row[attribute])
            for attribute in attributes
            if attribute == "Alta do episódio"
        )

        data.setdefault(year_month[0], {}).setdefault(year_month[1], 0)
        data[year_month[0]][year_month[1]] += highs_total
    return data


@ns_altas.route("/altas", strict_slashes=False)
class AltasHospitalar(Resource):
    def get(self):
        """
        Soma o atributo Alta do episódio da coleção Produção Conduta de todos os dados
        :return: Retorna um JSON agregado por ANO, MES
        """
        try:
            collection = "Produção Conduta"
            rows = aggregation_by(collection, ["Ano", "Mes"])
            data = agregacao_por_altas(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_altas.route("/altas/regions/<region>", strict_slashes=False)
class AltasHospitalarPorRegiao(Resource):
    def get(self, region):
        """
        Soma o atributo Alta do episódio da coleção Produção Conduta para uma Região de Saúde específica
        :param region: Região de Saúde para a qual a soma será calculada
        :return: Retorna um JSON agregado por ANO, MES
        """
        try:
            collection = "Produção Conduta"
            rows = aggregation_by(collection, ["Ano", "Mes"], [int(region)])
            data = agregacao_por_altas(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_altas.route("/altas/states/<state>", strict_slashes=False)
class AltasHospitalarPorEstado(Resource):
    def get(self, state):
        """
        Soma o atributo Alta do episódio da coleção Produção Conduta para um Estado específico

        :param state: A sigla do estado
        :return: Retorna um JSON agregado por ANO, MES
        """
        try:
            collection = "Produção Conduta"
            rows = aggregation_by(collection, ["Ano", "Mes"], None, [state])
            data = agregacao_por_altas(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_altas.route("/altas/cities/<ibge>", strict_slashes=False)
class AltasHospitalarPorCidade(Resource):
    """
    Soma o atributo Alta do episódio da coleção Produção Conduta para uma Cidade específica
    :param ibge: O código da IBEG da cidade
    :return: Retorna um JSON agregado por ANO, MES
    """

    def get(self, ibge):
        """
        Soma o atributo Alta do episódio da coleção Produção Conduta para uma Cidade específica
        :param ibge: O código IBGE da cidade
        :return: Retorna um JSON agregado por ANO, MES
        """
        try:
            collection = "Produção Conduta"
            rows = aggregation_by(
                collection, ["Ano", "Mes"], None, None, [int(ibge)]
            )
            data = agregacao_por_altas(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
