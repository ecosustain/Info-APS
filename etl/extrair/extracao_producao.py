"""Extração dos relatórios de produção do SISAB."""

import os
from datetime import datetime

from extrair.extracao import (
    carregar_xpaths,
    cria_driver,
    fazer_download,
    get_logger,
    seleciona_competencias,
    seleciona_xpath,
    selecionar_primeiro_item,
    verifica_arquivo,
    verifica_grupo,
)
from selenium.webdriver.common.by import By
from transformar import transf_producao

logger = get_logger("producao.log")


xpaths = carregar_xpaths()
LINK = xpaths["producao"]["link"]


# Carregar as configurações
transformacao_dir = os.getenv("TRANSFORMACAO_DIR", "data/transformacao")
download_dir = os.getenv("DOWNLOAD_DIR", "data/download")

# Gerar o nome do arquivo esperado dinamicamente
today = datetime.today().strftime("%Y-%m-%d")
PRODUCAO_FILENAME = "RelatorioSaudeProducao.csv"


def seleciona_producao(driver, linha, coluna, checkbox, nome_arq):
    """Seleciona a produção a ser extraída."""
    # Selecionar "Municípios" no dropdown de Linhas
    seleciona_xpath(driver, linha)
    # Selecionar "Coluna" no dropdown de Colunas
    seleciona_xpath(driver, coluna)
    # Verifica grupo 1
    verifica_grupo(driver, coluna, nome_arq)
    # Selecionar todos no checkbox da coluna
    selecionar_primeiro_item(driver, checkbox)


def executar_downloads_mes(linha, coluna, checkbox, nome_arq, num_meses=1000):
    """Executa o download dos relatórios de produção para cada mês."""
    verifica_arquivo(PRODUCAO_FILENAME)
    driver = cria_driver(LINK)
    competencias = seleciona_competencias(driver)
    falhas = 0
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
        logger.info("Processando o mês %s", mes)
        competencia.click()
        seleciona_producao(driver, linha, coluna, checkbox, nome_arq)
        if fazer_download(driver, mes, nome_arq):
            driver.refresh()
        else:
            falhas += 1
            driver.quit()
            if falhas > 3:
                logger.error("Muitas falhas, abortando")
                return False
            driver = cria_driver(LINK)
    logger.info("Script Finalizado")
    driver.quit()
