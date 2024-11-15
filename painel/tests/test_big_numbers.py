from unittest.mock import patch

import pytest
from dash.testing.application_runners import import_app
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


@pytest.fixture
def app():
    # Importar o aplicativo do arquivo app.py
    app = import_app("app")
    return app


cadastro = round(379197375 / 12)


@pytest.mark.parametrize(
    "expected_output",
    [(["75.0M", 2372, round(50039489 / cadastro * 1000)])],  # Exemplo de teste
)
@patch(
    "callbacks.initial_informations.big_number_ii.get_selected_year",
    return_value=2023,
)
def test_update_big_numbers_atend(
    mock_get_selected_year, app, dash_duo, expected_output
):
    # Inicie o servidor do app e espere até ele carregar
    dash_duo.start_server(app)

    # Selecionar o estado de São Paulo (SP) no dropdown
    dropdown = dash_duo.find_element(".Select-input input")
    dropdown.send_keys("SP")
    dropdown.send_keys(Keys.ENTER)

    # Esperar até que o indicador de carregamento desapareça
    dash_duo.wait_for_element("#loading-graphics", timeout=10)
    while dash_duo.find_element("#loading-graphics").is_displayed():
        dash_duo.wait_for_element("#loading-graphics", timeout=1)

    total_atendimentos_value = dash_duo.find_element(
        "#total-atendimentos"
    ).text
    normalizado_atendimentos_value = dash_duo.find_element(
        "#normalizado-atendimentos"
    ).text
    big_medicos_value = dash_duo.find_element("#big-medicos").text

    assert str(total_atendimentos_value) == str(
        expected_output[0]
    ), f"Valor de Total Atendimentos esperado: {expected_output[0]}, mas encontrou: {total_atendimentos_value}"
    assert (
        abs(int(normalizado_atendimentos_value) - expected_output[1]) <= 2
    ), f"Valor de Normalizado Atendimentos esperado: {expected_output[1]}, mas encontrou: {normalizado_atendimentos_value}"
    assert (
        abs(int(big_medicos_value) - expected_output[2]) <= 2
    ), f"Valor de Big Médicos esperado: {expected_output[2]}, mas encontrou: {big_medicos_value}"
