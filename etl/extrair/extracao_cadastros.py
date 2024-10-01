from selenium.webdriver.common.by import By

import etl.transformar.transformacao as transformacao
from etl.extrair.extracao import (
    carregar_xpaths,
    cria_driver,
    fazer_download,
    get_logger,
    seleciona_competencias,
    seleciona_xpath,
    verifica_arquivo,
)

logger = get_logger("cadastro.log")
xpaths = carregar_xpaths()
NOME_ARQ = xpaths["cadastro"]["nome_arq"]
CADASTRO_FILENAME = xpaths["cadastro"]["nome_arq_download"]
LINK = xpaths["cadastro"]["link"]


def download_cadastro(meses=1000):
    """Função para realizar o download dos cadastros de produção."""
    # Verifica se o arquivo já foi baixado
    verifica_arquivo(CADASTRO_FILENAME)
    # Cria o driver
    driver = cria_driver(LINK)
    # Clica no botão de competência
    competencias = seleciona_competencias(
        driver, xpaths["cadastro"]["competencia"]
    ).find_elements(By.TAG_NAME, "li")
    falhas = 0
    for i, competencia in enumerate(competencias):
        if i == meses:
            break
        if i > 0:
            competencias = seleciona_competencias(
                driver, xpaths["cadastro"]["competencia"]
            ).find_elements(By.TAG_NAME, "li")
            competencia = competencias[i]
        mes = competencia.text
        logger.info("Selecionando a competência %s", mes)
        competencia.click()
        seleciona_xpath(driver, xpaths["cadastro"]["municipio"])
        # Faz o download do relatório
        if fazer_download(
            driver,
            mes,
            NOME_ARQ,
            expected_filename=CADASTRO_FILENAME,
            xpath=xpaths["cadastro"]["download"],
        ):
            # Recarregar a página para a próxima competência
            driver.refresh()
        else:
            falhas += 1
            driver.quit()
            if falhas > 3:
                logger.error("Muitas falhas, abortando")
                return False
            driver = cria_driver(LINK)

    logger.info("Script Finalizado")
    # Fecha a janela do navegador
    driver.quit()


if __name__ == "__main__":
    logger.info(" -- Processando os cadastros  -- ")
    download_cadastro(3)
    logger.info("Script Finalizado")
    transformacao.main("cadastro")
