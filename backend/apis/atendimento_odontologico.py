from flask_restx import Resource, Namespace
from flask import make_response, jsonify

from database.collections import get_collection_attributes
from helpers.aggregation import aggregation_by

ns_atendimentos_odontologicos = Namespace("Atendimentos Odontológicos",
                                          description="Operações sobre o atributo 'Atendimento Odontológico' da coleção 'Tipo Produção'")


def agregacao_por_atendimento_odontologico(collection, rows):
    collection_attributes = get_collection_attributes(collection)
    data = {}

    for row in rows:
        year, month = row['_id']['Ano'], row['_id']['Mes']
        producao_total = sum(
            int(row[attribute]) for attribute in collection_attributes if attribute == "Atendimento Odontológico")

        data_year = data.get(year, {})
        data_year[month] = data_year.get(month, 0) + producao_total
        data[year] = data_year

    return data


@ns_atendimentos_odontologicos.route("/atendimentos_odontologicos", strict_slashes=False)
class AtendimentoOdontologico(Resource):
    def get(self):
        """
        Soma o atributo Atendimento Odontológico da coleção Tipo Produção de todos os anos, estados, regiões e cidades
        :return: Resposta JSON com coleções para a região e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro desconhecido
        """
        try:
            collection = 'Tipo Produção'
            rows = aggregation_by(collection, ["Ano", "Mes"])
            data = agregacao_por_atendimento_odontologico(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_odontologicos.route("/atendimentos_odontologicos/regions/<region>", strict_slashes=False)
class AtendimentoOdontologicoPorRegiao(Resource):
    def get(self, region):
        """
        Soma o atributo Atendimento Odontológico da coleção Tipo Produção por região de saúde
        :param region: Código da região de saúde
        :return: Retorna um JSON da colecão agregada por ANO, MES
        """
        try:
            collection = 'Tipo Produção'
            rows = aggregation_by(collection, ["Ano", "Mes"], [int(region)])
            data = agregacao_por_atendimento_odontologico(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_odontologicos.route("/atendimentos_odontologicos/states/<state>", strict_slashes=False)
class AtendimentoOdontologicoPorEstado(Resource):
    def get(self, state):
        """
        Soma o atributo Atendimento Odontológico da coleção Tipo Produção por estado
        :param state: A sigla do estado. AM, AL, etc
        :return: Retorna um JSON da colecão agregada por ANO, MES
        """
        try:
            collection = 'Tipo Produção'
            rows = aggregation_by(collection, ["Ano", "Mes"], None, [state])
            data = agregacao_por_atendimento_odontologico(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_odontologicos.route("/atendimentos_odontologicos/cities/<ibge>", strict_slashes=False)
class AtendimentoOdontologicoPorCidade(Resource):
    def get(self, ibge):
        """
        Soma o atributo Atendimento Odontológico da coleção Tipo Produção por cidade
        :param ibge: Código IBGE da cidade
        :return: Retorna um JSON da colecão agregada por ANO, MES
        """
        try:
            collection = 'Tipo Produção'
            rows = aggregation_by(collection, ["Ano", "Mes"], None, None, [int(ibge)])
            data = agregacao_por_atendimento_odontologico(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
