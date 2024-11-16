from time import sleep
from unittest.mock import patch

import pytest
from dash.testing.application_runners import import_app
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def app():
    # Importar o aplicativo do arquivo app.py
    app = import_app("app")
    return app


@pytest.fixture
def setup_app(app, dash_duo):
    """Fixture para subir o servidor, selecionar SP e esperar carregar"""
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

    sleep(1)

    # Selecionar o ano 2023 clicando no botão correspondente
    ano_button = dash_duo.find_element("#btn-ano-2023")
    ano_button.click()

    sleep(1)

    return dash_duo


cadastro = round(379197375 / 12)


@pytest.mark.parametrize(
    "expected_output",
    [
        (
            [
                "75.0M",
                2372,
                round(50039489 / cadastro * 1000),
                12,
                round(70556064 / cadastro * 1000),
                round(9228913 / cadastro * 1000),
            ]
        )  # Exemplo de teste
    ],
)
@patch(
    "callbacks.initial_informations.big_number_ii.get_selected_year",
    return_value=2023,
)
def test_update_big_numbers_atend(
    mock_get_selected_year, setup_app, expected_output
):
    """Testa a atualização dos números grandes de atendimentos"""
    dash_duo = setup_app

    total_atendimentos_value = dash_duo.find_element(
        "#total-atendimentos"
    ).text
    normalizado_atendimentos_value = dash_duo.find_element(
        "#normalizado-atendimentos"
    ).text
    big_medicos_value = dash_duo.find_element("#big-medicos").text
    big_encaminhamentos_value = dash_duo.find_element(
        "#big-encaminhamentos"
    ).text
    big_visitas_value = dash_duo.find_element("#big-visitas").text
    big_odontologicos_value = dash_duo.find_element("#big-odontologicos").text

    assert str(total_atendimentos_value) == str(
        expected_output[0]
    ), f"Valor de Total Atendimentos esperado: {expected_output[0]}, mas encontrou: {total_atendimentos_value}"
    assert (
        abs(int(normalizado_atendimentos_value) - expected_output[1]) <= 2
    ), f"Valor de Normalizado Atendimentos esperado: {expected_output[1]}, mas encontrou: {normalizado_atendimentos_value}"
    assert (
        abs(int(big_medicos_value) - expected_output[2]) <= 2
    ), f"Valor de Big Médicos esperado: {expected_output[2]}, mas encontrou: {big_medicos_value}"
    assert (
        abs(float(big_encaminhamentos_value) - expected_output[3]) <= 2
    ), f"Valor de Big Encaminhamentos esperado: {expected_output[3]}, mas encontrou: {big_encaminhamentos_value}"
    assert (
        abs(int(big_visitas_value) - expected_output[4]) <= 2
    ), f"Valor de Big Visitas esperado: {expected_output[4]}, mas encontrou: {big_visitas_value}"
    assert (
        abs(int(big_odontologicos_value) - expected_output[5]) <= 2
    ), f"Valor de Big Odontológicos esperado: {expected_output[5]}, mas encontrou: {big_odontologicos_value}"


def test_graficos_carregados(setup_app):
    """Testa se os gráficos foram carregados"""
    dash_duo = setup_app

    # Esperar até que o indicador de carregamento desapareça
    dash_duo.wait_for_element("#loading-graphics", timeout=10)
    while dash_duo.find_element("#loading-graphics").is_displayed():
        dash_duo.wait_for_element("#loading-graphics", timeout=1)

    sleep(5)

    # Verifique se os gráficos foram carregados
    grafico_1 = dash_duo.find_element("#chart_by_year")
    grafico_2 = dash_duo.find_element("#chart_by_year_profissionais")
    grafico_3 = dash_duo.find_element("#chart_encaminhamentos")

    assert grafico_1.is_displayed(), "Gráfico Atendimentos não foi carregado"
    assert grafico_2.is_displayed(), "Gráfico Profissionais não foi carregado"
    assert (
        grafico_3.is_displayed()
    ), "Gráfico encaminhamentos não foi carregado"

    # Verifique se os gráficos contêm dados
    assert "data" in grafico_1.get_attribute(
        "innerHTML"
    ), "Gráfico Atendimentos não contém dados"
    assert "data" in grafico_2.get_attribute(
        "innerHTML"
    ), "Gráfico Profissionais não contém dados"
    assert "data" in grafico_3.get_attribute(
        "innerHTML"
    ), "Gráfico Encaminhamentos não contém dados"
