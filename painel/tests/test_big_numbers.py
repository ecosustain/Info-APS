import pytest
from dash.testing.application_runners import import_app
from unittest.mock import patch


@pytest.fixture
def app():
    # Importa o arquivo principal app.py, onde o Dash é instanciado
    app = import_app("painel.app")  # Substitua pelo caminho completo do app
    return app

@pytest.mark.parametrize("expected_output", [
    (['', '', '356.9M', 2028, 1232])  # Exemplo de teste
])
@patch("callbacks.initial_informations.big_number_ii.get_selected_year", return_value=2023)
def test_update_big_numbers_atend(
    mock_get_selected_year, app, dash_duo, expected_output
):
    # Inicie o servidor do app e espere até ele carregar
    dash_duo.start_server(app)

    # Adicione uma espera para o carregamento dos indicadores
    dash_duo.wait_for_element("#indicador-atend-brasil", timeout=10)
    dash_duo.wait_for_element("#indicador-atend-estado", timeout=10)
    dash_duo.wait_for_element("#total-atendimentos", timeout=10)
    dash_duo.wait_for_element("#normalizado-atendimentos", timeout=10)
    dash_duo.wait_for_element("#big-medicos", timeout=10)

    # Esperar até que o indicador de carregamento desapareça
    dash_duo.wait_for_element("#loading-graphics", timeout=10)
    while dash_duo.find_element("#loading-graphics").is_displayed():
        dash_duo.wait_for_element("#loading-graphics", timeout=1)

    # Verifique os valores dos elementos usando o método `get_property`
    brasil_value = dash_duo.find_element("#indicador-atend-brasil").text
    estado_value = dash_duo.find_element("#indicador-atend-estado").text
    total_atendimentos_value = dash_duo.find_element("#total-atendimentos").text
    normalizado_atendimentos_value = dash_duo.find_element("#normalizado-atendimentos").text
    big_medicos_value = dash_duo.find_element("#big-medicos").text

    # Verifique se os valores dos elementos correspondem aos valores esperados
    assert str(brasil_value) == str(expected_output[0]), f"Valor do indicador Brasil esperado: {expected_output[0]}, mas encontrou: {brasil_value}"
    assert str(estado_value) == str(expected_output[1]), f"Valor do indicador Estado esperado: {expected_output[1]}, mas encontrou: {estado_value}"
    assert str(total_atendimentos_value) == str(expected_output[2]), f"Valor de Total Atendimentos esperado: {expected_output[2]}, mas encontrou: {total_atendimentos_value}"
    assert str(normalizado_atendimentos_value) == str(expected_output[3]), f"Valor de Normalizado Atendimentos esperado: {expected_output[3]}, mas encontrou: {normalizado_atendimentos_value}"
    assert str(big_medicos_value) == str(expected_output[4]), f"Valor de Big Médicos esperado: {expected_output[4]}, mas encontrou: {big_medicos_value}"
