from flask_restx import Resource, Namespace
from flask import make_response, jsonify

from config.global_vars import IGNORE_KEYS
from database.collections import get_collection_attributes
from helpers.aggregation import aggregation_by

ns_atendimentos_hospitalares = Namespace(
    "Atendimentos Hospitalares",
    description="Operações sobre os atributos da coleção 'Produção Profissionais Individual'",
)


def _add_data(datum, category, year, month, total):
    if year not in datum[category]:
        datum[category][year] = {}
    if month not in datum[category][year]:
        datum[category][year][month] = 0
    datum[category][year][month] += total


def aggregate_by_care(collection, rows):
    return_attributes = {
        "medico": "Médico",
        "enfermeiro": "Enfermeiro",
        "outros": "Outros",
    }
    collection_attributes = get_collection_attributes(collection)
    data = {"medico": {}, "enfermeiro": {}, "outros": {}}

    for row in rows:
        year = row["_id"]["Ano"]
        month = row["_id"]["Mes"]
        doctors_total, nurses_total, others_total = 0, 0, 0
        for attribute in collection_attributes:
            if attribute not in IGNORE_KEYS:
                if attribute == return_attributes["medico"]:
                    doctors_total += int(row[return_attributes["medico"]])
                elif attribute == return_attributes["enfermeiro"]:
                    nurses_total += int(row[return_attributes["enfermeiro"]])
                else:
                    others_total += int(row[attribute])
        _add_data(data, "medico", year, month, doctors_total)
        _add_data(data, "enfermeiro", year, month, nurses_total)
        _add_data(data, "outros", year, month, others_total)

    return data


@ns_atendimentos_hospitalares.route("/atendimentos", strict_slashes=False)
class AtendimentosHospitalar(Resource):

    def get(self):
        """
        Soma todos os atendimentos hospitalares, de todos os anos, dividivos em 3 tipos: médico, enfermeiro e outros e agregados por ANO, MES.
        :return: Coleção dividida em 3 categorias médico, enfermeiro e outros e agregadas por ANO e MES.
        """
        try:
            collection = "Produção Profissionais Individual"
            rows = aggregation_by(collection, ["Ano", "Mes"])
            data = aggregate_by_care(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_hospitalares.route(
    "/atendimentos/regions/<region>", strict_slashes=False
)
class AtendimentosHospitalarPorRegiao(Resource):

    def get(self, region):
        """
        Soma todos os atendimentos hospitalares, por região de saúde, dividivos em 3 tipos: médico, enfermeiro e outros e agregados por ANO, MES.
        :param region: O código IBGE da região
        :return: Coleção dividida em 3 categorias médico, enfermeiro e outros e agregadas por ANO e MES.
        """
        try:
            collection = "Produção Profissionais Individual"
            rows = aggregation_by(collection, ["Ano", "Mes"], [int(region)])
            data = aggregate_by_care(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_hospitalares.route(
    "/atendimentos/states/<state>", strict_slashes=False
)
class AtendimentosHospitalarPorEstado(Resource):
    def get(self, state):
        """
        Soma todos os atendimentos hospitalares, por unidade de federação, dividivos em 3 tipos: médico, enfermeiro e outros e agregados por ANO, MES.
        :param state: A sigla do estado
        :return: Coleção dividida em 3 categorias médico, enfermeiro e outros e agregadas por ANO e MES.
        """
        try:
            collection = "Produção Profissionais Individual"
            rows = aggregation_by(collection, ["Ano", "Mes"], None, [state])
            data = aggregate_by_care(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_hospitalares.route(
    "/atendimentos/cities/<ibge>", strict_slashes=False
)
class AtendimentosHospitalarPorCidade(Resource):
    def get(self, ibge):
        """
        Soma todos os atendimentos hospitalares, por cidade, dividivos em 3 tipos: médico, enfermeiro e outros e agregados por ANO, MES.
        :param ibge: O código IBGE da cidade
        :return: Coleção dividida em 3 categorias médico, enfermeiro e outros e agregadas por ANO e MES.
        """
        try:
            collection = "Produção Profissionais Individual"
            rows = aggregation_by(
                collection, ["Ano", "Mes"], None, None, [int(ibge)]
            )
            data = aggregate_by_care(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
