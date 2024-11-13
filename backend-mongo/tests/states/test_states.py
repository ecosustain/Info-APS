import unittest
from unittest.mock import patch

from apis.states import (State, StateSumByCollection,  # Módulo 'api'
                         StateSumByCollectionYear)
from flask import Flask
from flask_restx import Api


class StateTestCase(unittest.TestCase):

    def setUp(self):
        """Configura o ambiente de teste"""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(State, "/states")
        self.api.add_resource(
            StateSumByCollection, "/states/sum/<string:state>"
        )
        self.api.add_resource(
            StateSumByCollectionYear, "/states/sum/<string:state>/<int:year>"
        )
        self.client = self.app.test_client()

    # Testes para a classe State
    @patch("api.states.get_state")
    def test_get_states_success(self, mock_get_state):
        """Teste para verificar o sucesso ao buscar estados"""
        mock_get_state.return_value = [
            {"name": "California"},
            {"name": "Texas"},
        ]

        response = self.client.get("/states")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, [{"name": "California"}, {"name": "Texas"}]
        )

    @patch("api.states.get_state")
    def test_get_states_failure(self, mock_get_state):
        """Teste para verificar falha ao buscar estados"""
        mock_get_state.side_effect = Exception("Database error")

        response = self.client.get("/states")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"], "Database error")

    # Testes para a classe StateSumByCollection
    @patch("api.states.get_collection_sum_states")
    def test_get_collection_sum_by_state_success(
        self, mock_get_collection_sum_states
    ):
        """Teste para verificar o sucesso ao buscar soma de coleções por estado"""
        mock_get_collection_sum_states.return_value = [
            {"state": "California", "sum": 1500}
        ]

        response = self.client.get("/states/sum/California")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"state": "California", "sum": 1500}])

    @patch("api.states.get_collection_sum_states")
    def test_get_collection_sum_by_state_failure(
        self, mock_get_collection_sum_states
    ):
        """Teste para verificar falha ao buscar soma de coleções por estado"""
        mock_get_collection_sum_states.side_effect = Exception(
            "Collection sum error"
        )

        response = self.client.get("/states/sum/California")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"], "Collection sum error")

    # Testes para a classe StateSumByCollectionYear
    @patch("api.states.get_collection_sum_states_year")
    def test_get_collection_sum_by_state_year_success(
        self, mock_get_collection_sum_states_year
    ):
        """Teste para verificar o sucesso ao buscar soma de coleções por estado e ano"""
        mock_get_collection_sum_states_year.return_value = [
            {"state": "California", "year": 2021, "sum": 2500}
        ]

        response = self.client.get("/states/sum/California/2021")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, [{"state": "California", "year": 2021, "sum": 2500}]
        )

    @patch("api.states.get_collection_sum_states_year")
    def test_get_collection_sum_by_state_year_failure(
        self, mock_get_collection_sum_states_year
    ):
        """Teste para verificar falha ao buscar soma de coleções por estado e ano"""
        mock_get_collection_sum_states_year.side_effect = Exception(
            "Yearly collection sum error"
        )

        response = self.client.get("/states/sum/California/2021")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"], "Yearly collection sum error")


if __name__ == "__main__":
    unittest.main()
