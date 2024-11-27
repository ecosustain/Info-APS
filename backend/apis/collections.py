from config.global_vars import IGNORE_KEYS
from database.collections import get_collection_attributes, get_collection_count
from database.connection import db
from database.states import get_collection_sum_states, get_state
from flask import jsonify, make_response
from flask_restx import Namespace, Resource
from helpers.aggregation import aggregation_by
from helpers.collections import get_all_collections

ns_collection = Namespace(
    "Coleções Gerais",
    description="Operações sobre todas as coleções disponíveis",
)


def sum_values(value, key, total_sum):
    if isinstance(value, (int, float)):
        total_sum[key] = total_sum.get(key, 0) + value
    elif isinstance(value, str):
        value_without_dots = value.replace(".", "")
        if value_without_dots.isdigit():
            total_sum[key] = total_sum.get(key, 0) + int(value_without_dots)


def process_subdocument(value, key, total_sum):
    for sub_key, sub_value in value.items():
        composed_key = f"{key}.{sub_key}"
        sum_values(sub_value, composed_key, total_sum)


def get_collection_sum(collection_name, ignore_keys=None):
    collection = db[collection_name]
    ignore_keys = ignore_keys or IGNORE_KEYS
    documents = collection.find()
    total_sum = {}
    for document in documents:
        for key, value in document.items():
            if key not in ignore_keys:
                if isinstance(value, dict):
                    process_subdocument(value, key, total_sum)
                else:
                    sum_values(value, key, total_sum)
    return total_sum


@ns_collection.route("/collections/sum", strict_slashes=False)
class CollectionSumStates(Resource):
    def get(self):
        """
        Soma, por estado, todos os atributos de todas as coleções.
        :return: Retorna a soma, por estado, de todos os atributos de todas as coleções coletadas até o momento.
        """
        try:
            states = get_state()
            collections = get_collection_sum_states(states)
            if collections:
                return jsonify(collections)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_collection.route("/collections", strict_slashes=False)
class Collection(Resource):
    def get(self):
        """
        Lista as coleções disponíveis no sistema
        :return: Retorna uma lista das coleções disponíveis no sistema.
        """
        try:
            collections = get_all_collections()
            if collections:
                return jsonify(collections)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_collection.route("/collections/<collection>/sum", strict_slashes=False)
class CollectionSum(Resource):
    def get(self, collection):
        """
        Soma todos os atributos de uma coleção. Executar o método v1/collections para uma lista completa das coleções disponíveis no sistema.
        :param collection: Nome da coleção
        :return: A soma dos atributos de uma coleção
        """
        try:
            total = get_collection_sum(collection)
            return jsonify(total)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@ns_collection.route(
    "/collections/<collection>/<attribute>", strict_slashes=False
)
class CollectionSumByKey(Resource):
    def get(self, collection, attribute):
        """
        Soma um atributo específico de uma coleção específica de todos os períodos.
        :param collection: Nome da coleção
        :param attribute: Nome do atributo.
        :return: Soma do atributo no formato atributo: valor.
        """
        try:
            soma_total = get_collection_sum(collection)
            if attribute in soma_total:
                return jsonify({attribute: soma_total[attribute]})
            else:
                return (
                    jsonify(
                        {
                            "error": f"Chave '{attribute}' não encontrada na coleção {collection}."
                        }
                    ),
                    404,
                )
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@ns_collection.route(
    "/collections/<collection>/attributes", strict_slashes=False
)
class CollectionAttributes(Resource):
    def get(self, collection):
        """
        Lista todos os atributos de uma coleção
        :param collection: Nome da coleção
        :return: A lista de atributos da coleção
        """
        try:
            attributes = get_collection_attributes(collection)
            return jsonify(attributes)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_collection.route("/collections/<collection>/count", strict_slashes=False)
class CollectionAttributes(Resource):
    def get(self, collection):
        """
        Lista todos os atributos de uma coleção
        :param collection: Nome da coleção
        :return: A lista de atributos da coleção
        """
        try:
            count = get_collection_count(collection)
            return make_response(jsonify({"count": count}), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


def agregacao_por_collection(collection, rows, user_attributes):
    collection_attributes = get_collection_attributes(collection)
    data = {}

    for row in rows:
        year, month = row["_id"]["Ano"], row["_id"]["Mes"]
        producao_total = sum(
            int(row[attribute])
            for attribute in collection_attributes
            if attribute in user_attributes
        )

        data_year = data.get(year, {})
        data_year[month] = data_year.get(month, 0) + producao_total
        data[year] = data_year

    return data


@ns_collection.route("/<collection>/<attributes>", strict_slashes=False)
class Colecao(Resource):
    def get(self, collection, attributes):
        """
        Soma todos os atributos da coleção enviada, independentemente de estado, região ou cidade
        :param collection: Nome da coleção
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.
        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            user_attributes = attributes.split(",")
            rows = aggregation_by(collection, ["Ano", "Mes"])
            data = agregacao_por_collection(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_collection.route(
    "/<collection>/regions/<region>/<attributes>", strict_slashes=False
)
class ColecaoPorRegiao(Resource):
    def get(self, collection, region, attributes):
        """
        Soma os atributos da coleção enviada em uma região
        :param collection: Nome da coleção
        :param region: Código IBGE da região de saúde
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.
        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            user_attributes = attributes.split(",")
            rows = aggregation_by(collection, ["Ano", "Mes"], [int(region)])
            data = agregacao_por_collection(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_collection.route(
    "/<collection>/states/<state>/<attributes>", strict_slashes=False
)
class ColecaoPorEstado(Resource):
    def get(self, collection, state, attributes):
        """
        Soma os atributos da coleção enviada para um estado específico
        :param collection: Nome da collection
        :param state: A sigla do estado
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.
        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            user_attributes = attributes.split(",")
            rows = aggregation_by(collection, ["Ano", "Mes"], None, [state])
            data = agregacao_por_collection(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_collection.route(
    "/<collection>/cities/<ibge>/<attributes>", strict_slashes=False
)
class ColecaoPorCidade(Resource):
    def get(self, collection, ibge, attributes):
        """
        Soma os atributos da coleção enviada para uma cidade específica
        :param collection: Nome da collection
        :param ibge: Código IBGE da cidade
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.
        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            user_attributes = attributes.split(",")
            rows = aggregation_by(
                collection, ["Ano", "Mes"], None, None, [int(ibge)]
            )
            data = agregacao_por_collection(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(
                    jsonify({"error": "Coleções não encontradas"}), 404
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
