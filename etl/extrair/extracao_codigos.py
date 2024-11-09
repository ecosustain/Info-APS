"""Módulo para extrair os cids e ciaps do site do SISAB."""

import configparser
from datetime import datetime
from time import sleep

import transformar.transf_producao as transf_producao
from extrair.extracao import (
    carregar_xpaths,
    cria_driver,
    fazer_download,
    get_logger,
    seleciona_competencias,
    seleciona_xpath,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = get_logger("codigos.log")

xpaths = carregar_xpaths()
LINK = xpaths["producao"]["link"]


def expande_itens_por_pagina(driver):
    """Função para expandir o número de itens por página."""
    itens_por_pagina = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="dtBasicExample_length"]/label/select')
        )
    )
    itens_por_pagina.click()

    # Aguardar até que a opção de 100 itens esteja presente e clique nela
    opcao_100_itens = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="dtBasicExample_length"]/label/select/option[@value="100"]',
            )
        )
    )
    opcao_100_itens.click()


def seleciona_busca(busca, driver):
    """Função para selecionar a busca."""
    # Seleciona a barra de busca
    barra_busca = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="dtBasicExample_filter"]/label/input')
        )
    )
    for j, b in enumerate(busca):
        barra_busca.click()
        barra_busca.clear()
        barra_busca.send_keys(busca[j])

        # Seleciona todos os itens
        cids = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="dtBasicExample"]/tbody')
            )
        )
        for i, c in enumerate(cids.find_elements(By.TAG_NAME, "td")):
            cid = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f'//*[@id="dtBasicExample"]/tbody/tr[{i+1}]/td[1]/label/input',
                    )
                )
            )
            cid.click()


def clica_botao_cid(driver):
    """Função para clicar no botão cid."""
    cid_button = driver.find_element(
        By.XPATH,
        '//*[@id="btnAddCid"]',
    )
    driver.execute_script("arguments[0].click();", cid_button)


def seleciona_codigos(driver):
    """Função para selecionar os cids e ciaps."""
    # Seleciona "Municípios" no dropdown de Linhas
    seleciona_xpath(driver, '//*[@id="selectLinha"]/optgroup[1]/option[5]')
    # Seleciona "Coluna" no dropdown de Colunas
    seleciona_xpath(driver, '//*[@id="selectcoluna"]/optgroup[2]/option[7]')
    # Seleciona o botão cid e ciap
    clica_botao_cid(driver)
    # Mostra 100 itens por página
    expande_itens_por_pagina(driver)
    # Busca por febre
    seleciona_busca(["febre", "CIAP N01", "CIAP R05"], driver)


# Função para extrair os cids e ciaps do site do sisab
def extrair_codigos(num_meses=100):
    """Extrai os cids e ciaps do site do SISAB."""
    driver = cria_driver(LINK)
    # Seleciona as competencias
    competencias = seleciona_competencias(driver)
    falhas = 0
    # Itera sobre os meses
    for i, competencia in enumerate(
        competencias.find_elements(By.TAG_NAME, "li")
    ):
        if i == num_meses:
            break
        if i > 0:
            competencias = seleciona_competencias(driver).find_elements(
                By.TAG_NAME, "li"
            )
            competencia = competencias[i]
        mes = competencia.text
        competencia.click()
        # seleciona cids e ciaps
        seleciona_codigos(driver)
        # Faz o download
        if fazer_download(driver, mes, "producao_codigos"):
            driver.refresh()
        else:
            falhas += 1
            if falhas > 3:
                logger.error("Muitas falhas ao fazer download")
                break


if __name__ == "__main__":
    logger.info(" -- Iniciando extração de cids e ciaps --")
    extrair_codigos()
    transf_producao.main()
