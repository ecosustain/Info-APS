from flask_restx import Resource, Namespace
from flask import make_response, jsonify

from database.collections import get_collection_attributes
from helpers.aggregation import aggregation_by

ns_atendimentos_domiciliar = Namespace(
    "Atendimentos Domiciliar",
    description="Operações sobre o atributo 'Visita Domiciliar' da coleção 'Tipo Produção'",
)


def agregacao_por_atendimento_odontologico(collection, rows):
    collection_attributes = get_collection_attributes(collection)
    data = {}

    for row in rows:
        year, month = row["_id"]["Ano"], row["_id"]["Mes"]
        producao_total = sum(
            int(row[attribute])
            for attribute in collection_attributes
            if attribute == "Visita Domiciliar"
        )

        data_year = data.get(year, {})
        data_year[month] = data_year.get(month, 0) + producao_total
        data[year] = data_year

    return data


@ns_atendimentos_domiciliar.route("/visitas_domiciliar", strict_slashes=False)
class VistasDomiciliar(Resource):
    def get(self):
        """
        Soma os atributos que possuem Encaminhamento no nome da coleção Tipo Produção de todos os dados
        :return: Resposta JSON com coleções para a região e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro desconhecido
        """
        try:
            collection = "Tipo Produção"
            rows = aggregation_by(collection, ["Ano", "Mes"])
            data = agregacao_por_atendimento_odontologico(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_domiciliar.route(
    "/visitas_domiciliar/regions/<region>", strict_slashes=False
)
class VistasDomiciliarPorRegiao(Resource):
    def get(self, region):
        """
        Soma os atributos que possuem Encaminhamento no nome da coleção Tipo Produção
        :param region: Código da região utilizada para realizar a busca
        :return: Resposta JSON com coleções para a região e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro desconhecido
        """
        try:
            collection = "Tipo Produção"
            rows = aggregation_by(collection, ["Ano", "Mes"], [int(region)])
            data = agregacao_por_atendimento_odontologico(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_domiciliar.route(
    "/visitas_domiciliar/states/<state>", strict_slashes=False
)
class VistasDomiciliarPorEstado(Resource):
    def get(self, state):
        """
        Soma os atributos possuiem Encaminhamento no nome da coleção Tipo Produção
        :param region: O estado para o qual os producaos hospitalares serão recuperados
        :return: Resposta JSON com as coleções para o estado e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro
        """
        try:
            collection = "Tipo Produção"
            rows = aggregation_by(collection, ["Ano", "Mes"], None, [state])
            data = agregacao_por_atendimento_odontologico(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_domiciliar.route(
    "/visitas_domiciliar/cities/<ibge>", strict_slashes=False
)
class VistasDomiciliarPorCidade(Resource):
    def get(self, ibge):
        """
        Soma os atributos possuiem Encaminhamento no nome da coleção Tipo Produção para uma cidade específica

        :param region: Código IBGE da cidade para a qual deseja realizar a soma dos producaos
        :return: Resposta JSON com as coleções para o estado e ano especificados ou resposta de erro se as coleções não forem encontradas ou ocorrer um erro
        """
        try:
            collection = "Tipo Produção"
            rows = aggregation_by(
                collection, ["Ano", "Mes"], None, None, [int(ibge)]
            )
            data = agregacao_por_atendimento_odontologico(collection, rows)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
