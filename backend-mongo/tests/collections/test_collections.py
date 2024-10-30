import unittest
from unittest.mock import patch
from flask import Flask
from flask_restx import Api
from apis.collections import (
    Collection,
    CollectionSum,
    CollectionSumByKey,
)  # Módulo 'api'


class CollectionTestCase(unittest.TestCase):

    def setUp(self):
        """Configura o ambiente de teste"""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Collection, "/collections")
        self.api.add_resource(CollectionSum, "/collections/<collection>/sum")
        self.api.add_resource(
            CollectionSumByKey, "/collections/<collection>/<attribute>"
        )
        self.client = self.app.test_client()

    # Testes para a classe Collection
    @patch("api.collections.get_all_collections")
    def test_get_all_collections_success(self, mock_get_all_collections):
        """Teste para verificar o sucesso ao buscar todas as coleções"""
        mock_get_all_collections.return_value = [
            {"name": "Collection1"},
            {"name": "Collection2"},
        ]

        response = self.client.get("/collections")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, [{"name": "Collection1"}, {"name": "Collection2"}]
        )

    @patch("api.collections.get_all_collections")
    def test_get_all_collections_not_found(self, mock_get_all_collections):
        """Teste para verificar o retorno 404 quando nenhuma coleção é encontrada"""
        mock_get_all_collections.return_value = None

        response = self.client.get("/collections")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Coleções não encontradas")

    @patch("api.collections.get_all_collections")
    def test_get_all_collections_failure(self, mock_get_all_collections):
        """Teste para verificar falha ao buscar todas as coleções"""
        mock_get_all_collections.side_effect = Exception(
            "Erro ao buscar coleções"
        )

        response = self.client.get("/collections")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"], "Erro ao buscar coleções")

    # Testes para a classe CollectionSum
    @patch("api.collections.get_collection_sum")
    def test_get_collection_sum_success(self, mock_get_collection_sum):
        """Teste para verificar o sucesso ao buscar soma de uma coleção específica"""
        mock_get_collection_sum.return_value = {"Collection1": 5000}

        response = self.client.get("/collections/Collection1/sum")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Collection1": 5000})

    @patch("api.collections.get_collection_sum")
    def test_get_collection_sum_failure(self, mock_get_collection_sum):
        """Teste para verificar falha ao buscar soma de uma coleção"""
        mock_get_collection_sum.side_effect = Exception(
            "Erro ao buscar soma da coleção"
        )

        response = self.client.get("/collections/Collection1/sum")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["message"], "Internal Server Error")

    # Testes para a classe CollectionSumByKey
    @patch("api.collections.get_collection_sum")
    def test_get_collection_sum_by_key_success(self, mock_get_collection_sum):
        """Teste para verificar o sucesso ao buscar soma de uma coleção específica"""
        mock_get_collection_sum.return_value = {"Key1": 5000}

        response = self.client.get("/collections/Collection1/Key1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Key1": 5000})

    @patch("api.collections.get_collection_sum")
    def test_get_collection_sum_by_key_failure(self, mock_get_collection_sum):
        """Teste para verificar falha ao buscar soma de uma coleção"""
        mock_get_collection_sum.side_effect = Exception(
            "Internal Server Error"
        )

        response = self.client.get("/collections/Collection1/Key1")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["message"], "Internal Server Error")


if __name__ == "__main__":
    unittest.main()
