import configparser
import logging
import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Configura o logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("producao.log"), logging.StreamHandler()],
)

logger = logging.getLogger()

# Carregar o arquivo de configuração
config = configparser.ConfigParser()
config.read("config.ini")

# Diretório de download a partir do arquivo de configuração
download_dir = config["Paths"]["download_dir"]
destination_dir = config["Paths"]["transformacao_dir"]

# Gerar o nome do arquivo esperado dinamicamente
today = datetime.today().strftime("%Y-%m-%d")
producao_filename = "RelatorioSaudeProducao.csv"


def configurar_driver():
    """Configura e retorna o driver do Chrome."""
    options = Options()
    # options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_settings.popups": 0,  # Desativa popups de download
            "download.prompt_for_download": False,  # Não pergunta onde salvar
            "download.directory_upgrade": True,  # Atualiza o diretório automaticamente
            "safebrowsing.enabled": True,  # Habilita o Safe Browsing
            "profile.default_content_setting_values.automatic_downloads": 1,  # Permite múltiplos downloads
        },
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


def seleciona_xpath(driver, xpath):
    """Seleciona o elemento com o xpath"""
    try:
        seleciona = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(("xpath", xpath))
        )
        seleciona.click()
        return True
    except StaleElementReferenceException:
        return False


def selecionar_primeiro_item(driver, butao_xpath):
    """Seleciona a primeira coluna para download."""
    try:
        item_xpath = butao_xpath[:-6] + "ul/li[1]/a/label/input"
        # Encontra o botão e clica
        button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, butao_xpath))
        )
        button.click()
        # Seleciona o item
        item = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(("xpath", item_xpath))
        )
        if item.is_selected():
            return True
        item.click()
        return True
    except StaleElementReferenceException:
        return False


def clica_download(driver):
    """Clica no botão de download."""
    try:
        # Iniciar o download
        download_button = driver.find_element(
            By.XPATH,
            '//*[@id="j_idt44"]/div/div[1]/div/div[2]/div[2]/div[5]/div/div/div[2]/button',
        )
        driver.execute_script("arguments[0].click();", download_button)

        # Esperar o botão CSV estar clicável
        csv_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="j_idt44"]/div/div[1]/div/div[2]/div[2]/div[5]/div/div/div[2]/ul/li[2]/a',
                )
            )
        )
        driver.execute_script("arguments[0].click();", csv_button)
        return True
    except StaleElementReferenceException:
        return False


def espera_download(
    mes,
    nome_arq,
    download_dir=download_dir,
    expected_filename=producao_filename,
):
    """Espera o download do arquivo."""
    # Caminho completo para o arquivo esperado
    expected_file_path = os.path.join(download_dir, expected_filename)

    # Tempo máximo para esperar o download, em segundos
    timeout = 180
    start_time = time.time()

    # Esperar até que o arquivo apareça na pasta de downloads
    while True:
        if os.path.exists(expected_file_path):
            # Se o arquivo existir, verificar se o download foi concluído
            if not expected_file_path.endswith(".crdownload"):
                logger.info(f"Download completo: {expected_filename}")
                n_mes = mes.replace("/", "-")
                # Mover o arquivo para diretório de dados
                os.rename(
                    expected_file_path,
                    f"{destination_dir}/{nome_arq}_{n_mes}.csv",
                )
            return True
        elif time.time() - start_time > timeout:
            # Se o tempo de espera exceder o timeout, exibir uma mensagem de erro
            print(
                f"Tempo limite excedido para download de {expected_filename}."
            )
            return False
        time.sleep(1)  # Esperar 1 segundo antes de verificar novamente


def fazer_download(
    driver,
    mes,
    nome_arq,
    download_dir=download_dir,
    expected_filename=producao_filename,
):
    """Faz o download do relatório em formato CSV e espera até que o download esteja completo."""
    logger.info(f"Fazendo download do relatório para {mes}")

    # Inicia o download
    clica_download(driver)

    # Aguarda o arquivo ser baixado
    if not espera_download(mes, nome_arq, download_dir, expected_filename):
        return False
    return True


def seleciona_competencias(driver):
    """Seleciona a competência (mes/ano)"""

    # Clica no botão de de competência (mes/ano)
    competencia_element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="competencia"]/div/button')
        )
    )
    competencia_element.click()
    # Aguarda a lista de competências aparecer
    competencias = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located(
            ("xpath", '//*[@id="competencia"]/div/ul')
        )
    )
    return competencias


def executar_downloads_mes(linha, coluna, checkbox, nome_arq):
    driver = configurar_driver()
    logger.info("Iniciando o acesso a página de Producao do SISAB")
    driver.get(
        "https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/saude/RelSauProducao.xhtml"
    )
    # Esperar a página carregar
    wait = WebDriverWait(driver, 10)

    # Clica no botão de de competência (mes/ano)
    competencia_element = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="competencia"]/div/button')
        )
    )
    driver.execute_script("arguments[0].click();", competencia_element)

    competencias = wait.until(
        EC.presence_of_element_located(
            ("xpath", '//*[@id="competencia"]/div/ul')
        )
    )

    for j in range(len(competencias.find_elements(By.TAG_NAME, "li"))):
        # recarregar competencias
        if j > 0:
            competencias = seleciona_competencias(driver)
        for i, competencia in enumerate(
            competencias.find_elements(By.TAG_NAME, "li")
        ):
            if i == j:
                mes = competencia.text

                logger.info(f"Processando o mês {mes}")
                # Clica no botão de de competência (mes/ano)

                competencia.click()

                # Selecionar "Municípios" no dropdown de Linhas
                seleciona_xpath(driver, linha)

                # Selecionar "Condição Avaliada" no dropdown de Colunas
                seleciona_xpath(driver, coluna)

                # Selecionar todos em Problema / Condição Avaliada
                selecionar_primeiro_item(driver, checkbox)

                # Faz o download do relatório
                fazer_download(driver, mes, nome_arq)

                # Recarregar a página para a próxima competência
                driver.refresh()

    logger.info("Script Finalizado")
    # Fecha a janela do navegador
    driver.quit()


linhas = {
    "municipio": '//*[@id="selectLinha"]/optgroup[1]/option[5]',
    "competencia": '//*[@id="selectLinha"]/optgroup[1]/option[6]',
}

colunas = {
    "condicao": '//*[@id="selectcoluna"]/optgroup[2]/option[3]',
    "procedimento": '//*[@id="selectcoluna"]/optgroup[4]/option[1]',
}

checkbox = {
    "condicao": '//*[@id="filtrosAtendIndividual"]/div/div/div[3]/div/button',
    "procedimento": '//*[@id="filtrosProcedimento"]/div/div[1]/div[1]/div/button',
}


if __name__ == "__main__":
    executar_downloads_mes(
        linhas["municipio"],
        colunas["procedimento"],
        checkbox["procedimento"],
        "producao_procedimento",
    )
