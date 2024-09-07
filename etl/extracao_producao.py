import configparser
from datetime import datetime

import transf_producao
from extracao import (
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

logger = get_logger("producao.log")


xpaths = carregar_xpaths()
LINK = xpaths["producao"]["link"]


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
PRODUCAO_FILENAME = "RelatorioSaudeProducao.csv"


def executar_downloads_mes(linha, coluna, checkbox, nome_arq, meses=1000):
    """Executa o download dos relatórios de produção para cada mês."""
    verifica_arquivo(PRODUCAO_FILENAME)
    # Inicializa o driver
    driver = cria_driver(LINK)
    competencias = seleciona_competencias(driver)
    falhas = 0
    for i, competencia in enumerate(
        competencias.find_elements(By.TAG_NAME, "li")
    ):
        if i == meses:
            break
        if i > 0:
            competencias = seleciona_competencias(driver).find_elements(
                By.TAG_NAME, "li"
            )
            competencia = competencias[i]
        mes = competencia.text
        logger.info("Processando o mês %s", mes)
        # Clica no botão de de competência (mes/ano)
        competencia.click()

        # Selecionar "Municípios" no dropdown de Linhas
        seleciona_xpath(driver, linha)

        # Selecionar "Coluna" no dropdown de Colunas
        seleciona_xpath(driver, coluna)

        # Verifica grupo 1
        verifica_grupo(driver, coluna, nome_arq)

        # Selecionar todos no checkbox da coluna
        selecionar_primeiro_item(driver, checkbox)

        # Faz o download do relatório
        if fazer_download(driver, mes, nome_arq):
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


# Lista de produções a serem extraídas - Incluir aqui as produções que deseja extrair
lista = [
    "producao_tipo",
    "producao_profissionais_odontologico",
    "producao_conduta",
]


if __name__ == "__main__":
    for producao in lista:
        logger.info(f" -- Processando a produção {producao}  -- ")
        executar_downloads_mes(
            xpaths["producao"][
                "municipio"
            ],  # Acessa o XPath da linha (Município)
            xpaths[producao]["coluna"],  # Acessa o XPath da coluna
            xpaths[producao]["checkbox"],  # Acessa o XPath do checkbox
            producao,
            meses=100,
        )
        transf_producao.main()
    logger.info("Script Finalizado")
