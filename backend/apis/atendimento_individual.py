from flask_restx import Resource, Namespace
from flask import make_response, jsonify

from database.cities import get_population
from database.collections import get_collection_attributes
from helpers.aggregation import aggregation_by, aggregation_big_numbers

ns_atendimentos_individuais = Namespace("Atendimentos Individuais",
                                        description="Operações sobre os atributos da coleção Problemas")


def agregacao_por_atendimento_individual(collection, rows, user_attributes):
    collection_attributes = get_collection_attributes(collection)
    data = {}

    for row in rows:
        year, month = row['_id']['Ano'], row['_id']['Mes']
        producao_total = sum(
            int(row[attribute]) for attribute in collection_attributes if attribute in user_attributes)

        data_year = data.get(year, {})
        data_year[month] = data_year.get(month, 0) + producao_total
        data[year] = data_year

    return data

def agregacao_por_atendimento_numbers(collection, rows, user_attributes):
    collection_attributes = get_collection_attributes(collection)
    data = {}

    for row in rows:
        try:
            uf = row['_id']['Uf']
            region = row['_id']['region']
            year = row['_id']['Ano']
            month = row['_id']['Mes']
            city = row['_id']['Municipio']
            populacao = row['media_cadastros']

            # Calcula a produção total para o município
            producao_total = sum(
                int(row[attribute]) for attribute in collection_attributes if attribute in user_attributes
            )

            # Calcula o total por mil habitantes
            producao_por_mil_habitantes = (producao_total / populacao) * 1000 if populacao > 0 else 0

            # Organiza os dados em níveis de UF > Region > Year > Month > City
            if uf not in data:
                data[uf] = {}
            if region not in data[uf]:
                data[uf][region] = {}
            if year not in data[uf][region]:
                data[uf][region][year] = {}
            # if month not in data[uf][region][year]:
            #     data[uf][region][year][month] = {}

            # Define o valor da cidade com producao_por_mil_habitantes
            # data[uf][region][year][month][city] = producao_por_mil_habitantes
            data[uf][region][year][city] = producao_por_mil_habitantes

        except Exception as ex:
            print(ex)

    return data


@ns_atendimentos_individuais.route("/atendimento_individual/<attributes>", strict_slashes=False)
class AtendimentoIndividual(Resource):
    def get(self, attributes):
        """
        Soma todos os atributos enviados encontrados na coleção Problemas, independentemente de estado, região ou cidade
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.

        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            collection = 'Problemas'
            user_attributes = attributes.split(",")
            rows = aggregation_by(collection, ["Ano", "Mes"])
            data = agregacao_por_atendimento_individual(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_individuais.route("/atendimento_individual/regions/<region>/<attributes>", strict_slashes=False)
class AtendimentoIndividualPorRegiao(Resource):
    def get(self, region, attributes):
        """
        Soma os atributos enviados encontrados na coleção Problemas para a região enviada
        :param region: Código da região utilizada para realizar a busca
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.
        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            user_attributes = attributes.split(",")
            collection = 'Problemas'
            rows = aggregation_by(collection, ["Ano", "Mes"], [int(region)])
            data = agregacao_por_atendimento_individual(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_individuais.route("/atendimento_individual/states/<state>/<attributes>", strict_slashes=False)
class AtendimentoIndividualPorEstado(Resource):
    def get(self, state, attributes):
        """
        Soma os atributos enviados encontrados na coleção Problemas para um estado específico
        :param state: A sigla do estado
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.

        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            collection = 'Problemas'
            user_attributes = attributes.split(",")
            rows = aggregation_by(collection, ["Ano", "Mes"], None, [state])
            data = agregacao_por_atendimento_individual(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_individuais.route("/atendimento_individual/cities/<ibge>/<attributes>", strict_slashes=False)
class AtendimentoIndividualPorCidade(Resource):
    def get(self, ibge, attributes):
        """
        Soma os atributos enviados encontrados na coleção Problemas para uma cidade específica
        :param ibge: Código IBGE da cidade
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.

        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            collection = 'Problemas'
            user_attributes = attributes.split(",")
            rows = aggregation_by(collection, ["Ano", "Mes"], None, None, [int(ibge)])
            data = agregacao_por_atendimento_individual(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_individuais.route("/atendimento_individual/cities/<ibge>/<attributes>", strict_slashes=False)
class AtendimentoIndividualPorCidade(Resource):
    def get(self, ibge, attributes):
        """
        Soma os atributos enviados encontrados na coleção Problemas para uma cidade específica
        :param ibge: Código IBGE da cidade
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.

        :return: Retorna um JSON com a coleção agregada por ANO, MES
        """
        try:
            collection = 'Problemas'
            user_attributes = attributes.split(",")
            rows = aggregation_by(collection, ["Ano", "Mes"], None, None, [int(ibge)])
            data = agregacao_por_atendimento_individual(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_individuais.route("/atendimento_individual/numbers/<attributes>", strict_slashes=False)
class AtendimentoIndividual(Resource):
    def get(self, attributes):
        """
        Soma todos os atributos enviados encontrados na coleção Problemas, independentemente de estado, região ou cidade por 1000 habitantes
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.

        :return: Retorna um JSON com a coleção agregada por Uf, Região, ANO, MES
        """
        try:
            collection = 'Problemas'
            user_attributes = attributes.split(",")
            rows = aggregation_big_numbers(collection, ["Uf", "Ano", "Mes", "region", "Municipio"], user_attributes=user_attributes)
            data = agregacao_por_atendimento_numbers(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_individuais.route("/atendimento_individual/numbers/regions/<region>/<attributes>",
                                   strict_slashes=False)
class AtendimentoIndividualPorRegiao(Resource):
    def get(self, region, attributes):
        """
        Soma os atributos enviados encontrados na coleção Problemas para a região enviada por 1000 habitantes
        :param region: Código da região utilizada para realizar a busca
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.
        :return: Retorna um JSON com a coleção agregada por Uf, Região, ANO, MES
        """
        try:
            user_attributes = attributes.split(",")
            collection = 'Problemas'
            rows = aggregation_big_numbers(collection, ["Uf", "Ano", "Mes", "region", "Municipio"], regions=[int(region)], user_attributes=user_attributes)
            data = agregacao_por_atendimento_numbers(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_individuais.route("/atendimento_individual/numbers/states/<state>/<attributes>", strict_slashes=False)
class AtendimentoIndividualPorEstado(Resource):
    def get(self, state, attributes):
        """
        Soma os atributos enviados encontrados na coleção Problemas para um estado específico por 1000 habitantes
        :param state: A sigla do estado
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.

        :return: Retorna um JSON com a coleção agregada por Uf, Região, ANO, MES
        """
        try:
            collection = 'Problemas'
            user_attributes = attributes.split(",")
            rows = aggregation_big_numbers(collection, ["Uf", "Ano", "Mes", "region", "Municipio"], states=[state], user_attributes=user_attributes)
            data = agregacao_por_atendimento_numbers(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_atendimentos_individuais.route("/atendimento_individual/numbers/cities/<ibge>/<attributes>", strict_slashes=False)
class AtendimentoIndividualPorCidade(Resource):
    def get(self, ibge, attributes):
        """
        Soma os atributos enviados encontrados na coleção Problemas para uma cidade específica por 1000 habitantes
        :param ibge: Código IBGE da cidade
        :param attributes: Atributos que serão somados (separar por vígulas) dentre os disponíveis: Asma,Desnutrição,Diabetes,DPOC,Hipertensão arterial, etc. Executar o métodos em Coleções Gerais: api/v1/collections/\<collection\>/attributes, para uma lista completa dos atributos. Nesse caso, collection=Problemas.

        :return: Retorna um JSON com a coleção agregada por Uf, Região, ANO, MES
        """
        try:
            collection = 'Problemas'
            user_attributes = attributes.split(",")
            rows = aggregation_big_numbers(collection, ["Uf", "Ano", "Mes", "region", "Municipio"], cities=[int(ibge)], user_attributes=user_attributes)
            data = agregacao_por_atendimento_numbers(collection, rows, user_attributes)

            if data:
                return jsonify(data)
            else:
                return make_response(jsonify({"error": "Coleções não encontradas"}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


