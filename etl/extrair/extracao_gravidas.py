"""Extração dos relatórios de grávidas do SISAB."""

import configparser
from datetime import datetime

import transformar.transf_producao as transf_producao
from extrair.extracao import (carregar_xpaths, cria_driver, fazer_download,
                              get_logger, seleciona_competencias,
                              seleciona_xpath, verifica_arquivo)
from selenium.webdriver.common.by import By

logger = get_logger("producao_gravidas.log")


xpaths = carregar_xpaths()
LINK = xpaths["gravidas"]["link"]
FILENAME = xpaths["gravidas"]["nome_arq"]


def carregar_configuracoes():
    """Carrega as configurações do arquivo config.ini"""
    # Carregar o arquivo de configuração
    config = configparser.ConfigParser()
    config.read("config.ini")
    # Diretórios de destino e download
    transformacao_dir = config["Paths"]["transformacao_dir"]
    download_dir = config["Paths"]["download_dir"]
    return transformacao_dir, download_dir


# Carregar as configurações
transformacao_dir, download_dir = carregar_configuracoes()

# Gerar o nome do arquivo esperado dinamicamente
today = datetime.today().strftime("%Y-%m-%d")
PRODUCAO_FILENAME = "gravidas"


def seleciona_producao(driver, linha, coluna):
    """Seleciona linha e coluna a ser extraída."""
    # Selecionar "Municípios" no dropdown de Linhas
    seleciona_xpath(driver, linha)
    # Selecionar "Indicador" no dropdown de Colunas
    seleciona_xpath(driver, coluna)


def executar_downloads_mes(linha, coluna, nome_arq, num_meses=1000):
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
        seleciona_producao(driver, linha, coluna)
        if fazer_download(
            driver,
            mes,
            nome_arq,
            xpath='//*[@id="j_idt44"]/div/div[1]/div/div[2]/div[2]/div[4]/div/div/div/div/button',
        ):
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


if __name__ == "__main__":
    logger.info(" -- Extraindo grávidas-- ")
    """executar_downloads_mes(
        xpaths["gravidas"]["municipio"],
        xpaths["gravidas"]["coluna"],
        PRODUCAO_FILENAME
    )"""
    transf_producao.main()
    logger.info("Script Finalizado")
