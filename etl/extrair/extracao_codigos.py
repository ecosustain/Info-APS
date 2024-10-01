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
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Configura o logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("teste.log"), logging.StreamHandler()],
)

logger = logging.getLogger()

# Carregar o arquivo de configuração
config = configparser.ConfigParser()
config.read("config.ini")

# Diretórios de destino e download
transformacao_dir = config["Paths"]["transformacao_dir"]
download_dir = config["Paths"]["download_dir"]

# Gerar o nome do arquivo esperado dinamicamente
today = datetime.today().strftime("%Y-%m-%d")
PRODUCAO_FILENAME = "RelatorioSaudeProducao.csv"


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
    expected_filename=PRODUCAO_FILENAME,
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
                    f"{transformacao_dir}/{nome_arq}_{n_mes}.csv",
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
    expected_filename=PRODUCAO_FILENAME,
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


def cria_driver():
    """Cria o driver do Chrome."""
    driver = configurar_driver()
    logger.info("Iniciando o acesso a página de Producao do SISAB")
    driver.get(
        "https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/saude/RelSauProducao.xhtml"
    )
    return driver


def seleciona_cid(driver, h):
    """Seleciona o SIGTAB"""
    # Clicar no botão de adicionar SIGTAB
    cid_button = driver.find_element(
        By.XPATH,
        '//*[@id="btnAddCid"]',
    )

    driver.execute_script("arguments[0].click();", cid_button)

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

    for j in range(150):
        if j == h:
            # Selecionar todos os CIDs
            cids = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="dtBasicExample"]/tbody')
                )
            )
            for i in range(len(cids.find_elements(By.TAG_NAME, "td"))):
                cid = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f'//*[@id="dtBasicExample"]/tbody/tr[{i+1}]/td[1]/label/input',
                        )
                    )
                )
                cid.click()

        # Clica na próxima página
        proxima_pagina = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="dtBasicExample_next"]/a')
            )
        )

        proxima_pagina.click()

        if j == h:
            # Clica no botão de concluir
            concluir_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="modal-default-cid"]/div/div/div[2]/button[2]',
                    )
                )
            )
            concluir_button.click()
            break

    return True


def seleciona_sigtap(driver, h):
    """Seleciona o SIGTAP"""
    # Clicar no botão de adicionar SIGTAB
    cid_button = driver.find_element(
        By.XPATH,
        '//*[@id="btnAddSigtap"]',
    )

    driver.execute_script("arguments[0].click();", cid_button)

    itens_por_pagina = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="td-ls-sigtap_length"]/label/select')
        )
    )
    itens_por_pagina.click()

    # Aguardar até que a opção de 100 itens esteja presente e clique nela
    opcao_100_itens = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="[@id="td-ls-sigtap_length"]/label/select/option[@value="100"]',
            )
        )
    )
    opcao_100_itens.click()

    for j in range(48):
        if j == h:
            # Selecionar todos os CIDs
            cids = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="td-ls-sigtap"]/tbody')
                )
            )
            for i in range(len(cids.find_elements(By.TAG_NAME, "td"))):
                cid = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f'//*[@id="td-ls-sigtap"]/tbody/tr[{i+1}]/td[1]/label/input',
                        )
                    )
                )
                cid.click()

        # Clica na próxima página
        proxima_pagina = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="td-ls-sigtap_next"]/a')
            )
        )

        proxima_pagina.click()

        if j == h:
            # Clica no botão de concluir
            concluir_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="modal-default-sigtap"]/div/div/div[2]/button[2]',
                    )
                )
            )
            concluir_button.click()
            break

    return True


def todos_cid():
    """Executa o download dos relatórios de produção para cada mês."""
    # Inicializa o driver
    driver = cria_driver()
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
    competencias.click()
    for i in range(150):
        try:
            if i > 0:
                competencias = seleciona_competencias(driver)

            for k, competencia in enumerate(
                competencias.find_elements(By.TAG_NAME, "li")[:7]
            ):
                competencia.click()

            # Selecionar "Municípios" no dropdown de Linhas
            seleciona_xpath(
                driver, '//*[@id="selectLinha"]/optgroup[1]/option[5]'
            )

            # Selecionar "CID" no dropdown de Colunas
            seleciona_xpath(
                driver, '//*[@id="selectcoluna"]/optgroup[2]/option[7]'
            )

            # Selecionar o CIDs
            seleciona_cid(driver, i)

            fazer_download(driver, f"12_meses_{i}", "producao_cid")
            driver.quit()
            driver = cria_driver()
        except Exception as e:
            print("Erro na execução: ", i)
            print(e)
            driver.quit()
            driver = cria_driver()
            continue

    time.sleep(10)
    logger.info("Script Finalizado")
    # Fecha a janela do navegador
    driver.quit()


def todos_sigtap():
    """Executa o download dos relatórios de produção para cada mês."""
    # Inicializa o driver
    driver = cria_driver()
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
    competencias.click()
    for i in range(150):
        try:
            if i > 0:
                competencias = seleciona_competencias(driver)

            for k, competencia in enumerate(
                competencias.find_elements(By.TAG_NAME, "li")[:7]
            ):
                competencia.click()

            # Selecionar "Municípios" no dropdown de Linhas
            seleciona_xpath(
                driver, '//*[@id="selectLinha"]/optgroup[1]/option[5]'
            )

            # Selecionar "CID" no dropdown de Colunas
            seleciona_xpath(
                driver, '//*[@id="selectcoluna"]/optgroup[4]/option[3]'
            )

            # Selecionar o CIDs
            seleciona_cid(driver, i)

            fazer_download(driver, f"12_meses_{i}", "producao_sigtap")
            driver.quit()
            driver = cria_driver()
        except Exception as e:
            print("Erro na execução: ", i)
            print(e)
            driver.quit()
            driver = cria_driver()
            continue

    time.sleep(10)
    logger.info("Script Finalizado")
    # Fecha a janela do navegador
    driver.quit()


todos_sigtap()
