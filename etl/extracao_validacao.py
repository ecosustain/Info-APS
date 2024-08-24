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

"""
Web Scraping com Selenium e Python para a página de validação do SISAB

Necessidades
- Modularizar
- Tratar exceções
- Adicionar logs
- Adicionar documentação
- Adicionar testes
- Adicionar requirements
- Adicionar Dockerfile
- Adicionar Makefile
- Adicionar CI/CD
"""


# Configura o logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("automation.log"), logging.StreamHandler()],
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
validacao_filename = f"RelatorioValidacao-{today}.csv"


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


def controle_download(arquivo="controle_validacao.txt"):
    """Lê o arquivo de controle e retorna uma lista com os estados e meses já processados."""
    with open(arquivo, "r") as controle:
        estado_mes = controle.read().splitlines()
    return estado_mes


def selecionar_municipios_dividido(driver, metade):
    """Seleciona os municípios para o estado de SP."""
    municipios_button = driver.find_element(
        By.XPATH, '//*[@id="regioes"]/div/button'
    )
    driver.execute_script("arguments[0].click();", municipios_button)
    time.sleep(1)  # Esperar o dropdown ser exibido

    municipio_elements = driver.find_elements(
        By.XPATH, '//*[@id="regioes"]/div/ul/li/a/label/input'
    )
    if metade:
        for checkbox in municipio_elements[:400]:
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", checkbox
            )
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
    else:
        # Desmarcar todos os municípios
        for checkbox in municipio_elements[:400]:
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", checkbox
            )
            if checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)
        # Selecionar os municípios restantes
        for checkbox in municipio_elements[400:]:
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", checkbox
            )
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(1)


def extrai_dividido(
    driver, estado, mes_text, controle_arquivo="controle_validacao.txt"
):
    """Seleciona os municípios dos estados grandes."""
    # Primeira metade
    selecionar_municipios_dividido(driver, True)
    selecionar_colunas(driver)
    if not fazer_download(driver, estado, mes_text):
        return "ERRO"
    # Segunda metade
    selecionar_municipios_dividido(driver, False)
    if not fazer_download(driver, estado, mes_text, dividido=True):
        return "ERRO"

    # Registrar o download no controle
    with open(controle_arquivo, "a") as controle:
        controle.write(f"{estado}_{mes_text}\n")

    # Recarregar a página para o próximo estado
    recarregar_pagina(driver)
    return "DIVIDIDO"


def selecionar_municipios(driver, estado_text, mes_text):
    """Seleciona os municípios para o estado fornecido e lida com possíveis exceções."""
    try:
        municipios_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="regioes"]/div/button')
            )
        )
        driver.execute_script("arguments[0].click();", municipios_button)

        municipio_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="regioes"]/div/ul/li/a/label/input')
            )
        )

        print("MUNICIPIOS: ", len(municipio_elements))
        if len(municipio_elements) > 450:
            logger.info(
                f"O estado {estado_text} possui mais de 450 municípios"
            )
            return extrai_dividido(driver, estado_text, mes_text)

        for checkbox in municipio_elements:
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", checkbox
            )
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)
        return "OK"

    except StaleElementReferenceException:
        logger.error(
            "StaleElementReferenceException: O elemento não está mais disponível. Tentando novamente."
        )
        return selecionar_municipios(
            driver, estado_text, mes_text
        )  # Tenta novamente após a exceção

    except Exception as e:
        logger.error(f"Erro ao selecionar municípios: {e}")
        return "ERRO"


def selecionar_colunas(driver):
    """Seleciona a primeira coluna para download."""
    colunas_button = driver.find_element(
        By.XPATH, '//*[@id="filtrosLinhaColunaRelatorio"]/div/button'
    )
    driver.execute_script("arguments[0].click();", colunas_button)
    time.sleep(1)

    coluna_element = driver.find_element(
        By.XPATH,
        '//*[@id="filtrosLinhaColunaRelatorio"]/div/ul/li[1]/a/label/input',
    )
    if not coluna_element.is_selected():
        driver.execute_script("arguments[0].click();", coluna_element)
    time.sleep(1)


def fazer_download(
    driver,
    estado,
    mes,
    download_dir=download_dir,
    expected_filename=validacao_filename,
    dividido=False,
):
    """Faz o download do relatório em formato CSV e espera até que o download esteja completo."""
    logger.info(f"Fazendo download do relatório para {estado} em {mes}")
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

    # Caminho completo para o arquivo esperado
    expected_file_path = os.path.join(download_dir, expected_filename)

    # Tempo máximo para esperar o download, em segundos
    timeout = 60
    start_time = time.time()

    # Esperar até que o arquivo apareça na pasta de downloads
    while True:
        if os.path.exists(expected_file_path):
            # Se o arquivo existir, verificar se o download foi concluído
            if not expected_file_path.endswith(".crdownload"):
                print(f"Download completo: {expected_filename}")
                n_mes = mes.replace("/", "-")
                # Mover o arquivo para diretório de dados
                if dividido:
                    os.rename(
                        expected_file_path,
                        f"{destination_dir}/validacao_{estado}_{n_mes}_1.csv",
                    )
                    return True
                else:
                    os.rename(
                        expected_file_path,
                        f"{destination_dir}/validacao_{estado}_{n_mes}.csv",
                    )
                return True
        elif time.time() - start_time > timeout:
            # Se o tempo de espera exceder o timeout, exibir uma mensagem de erro
            print(
                f"Tempo limite excedido para download de {expected_filename}."
            )
            return False
        time.sleep(1)  # Esperar 1 segundo antes de verificar novamente


def recarregar_pagina(driver, estado_index=1, mes_index=1):
    """Recarrega a página e reposiciona o dropdown no estado e mês corretos."""
    driver.refresh()
    time.sleep(
        3
    )  # Espera para garantir que a página seja totalmente carregada

    # Selecionar "Municípios" no dropdown de unidades geográficas
    unid_geo = Select(driver.find_element(By.ID, "unidGeo"))
    unid_geo.select_by_visible_text("Municípios")

    competencia = Select(driver.find_element(By.NAME, "j_idt70"))
    competencia.select_by_index(mes_index)

    wait = WebDriverWait(driver, 10)
    estados_element = wait.until(
        EC.presence_of_element_located((By.ID, "estadoMunicipio"))
    )

    estados = Select(estados_element)
    return estados.options[estado_index]


def processar_estado_mes(
    driver,
    estado,
    mes_text,
    estado_index,
    mes_index,
    controle_arquivo="controle_validacao.txt",
):
    """Processa o download de dados para um estado e mês específico."""
    if f"{estado.text}_{mes_text}" in controle_download(controle_arquivo):
        logger.info(f"Pulando download de {estado.text} para {mes_text}")
        return False

    # Clicar no estado
    estado.click()
    estado_text = estado.text
    logger.info(f"Processando o estado {estado_text} para {mes_text}")

    saida_municipios = selecionar_municipios(driver, estado_text, mes_text)

    if saida_municipios == "OK":
        selecionar_colunas(driver)
        if not fazer_download(driver, estado_text, mes_text):
            return False
        time.sleep(5)
        # Registrar o download no controle
        with open(controle_arquivo, "a") as controle:
            controle.write(f"{estado_text}_{mes_text}\n")

        # Recarregar a página para o próximo estado
        recarregar_pagina(driver, estado_index, mes_index)
        return True
    if saida_municipios == "DIVIDIDO":
        return True
    logger.info(
        f"Erro ao processar {estado_text} para {mes_text}. Saida: {saida_municipios}"
    )
    return False


def executar_downloads():
    driver = configurar_driver()
    logger.info("Iniciando o acesso a página do SISAB")
    driver.get(
        "https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/envio/RelValidacao.xhtml"
    )
    # Esperar a página carregar
    wait = WebDriverWait(driver, 10)

    # Selciona o dropdown de competência (mes/ano)
    competencia_element = wait.until(
        EC.element_to_be_clickable((By.NAME, "j_idt70"))
    )
    competencia = Select(competencia_element)

    for j in range(len(competencia.options)):
        try:
            mes_text = competencia.options[j].text
        except StaleElementReferenceException:
            competencia = Select(
                wait.until(EC.element_to_be_clickable((By.NAME, "j_idt70")))
            )
            mes_text = competencia.options[j].text

        # Adiciona no log o mês que está sendo processado
        logger.info(f"Processando o mês {mes_text}")

        # Seleciona o mês no dropdown de competência
        competencia.select_by_index(j)

        # Selecionar "Municípios" no dropdown de unidades geográficas
        unid_geo_element = wait.until(
            EC.element_to_be_clickable((By.ID, "unidGeo"))
        )
        unid_geo = Select(unid_geo_element)
        unid_geo.select_by_visible_text("Municípios")

        estados_element = wait.until(
            EC.presence_of_element_located((By.ID, "estadoMunicipio"))
        )

        estados = Select(estados_element)

        for i in range(1, len(estados.options)):
            try:
                estado = estados.options[i]
            except StaleElementReferenceException:
                estados = Select(
                    wait.until(
                        EC.presence_of_element_located(
                            (By.ID, "estadoMunicipio")
                        )
                    )
                )
                estado = estados.options[i]
            # try:
            if not processar_estado_mes(driver, estado, mes_text, i, j):
                continue
            # except Exception as e:
            #    # Handle the specific exception here
            #    logger.error(f"Erro ao processar {estado_text} para {mes_text}: {e}")
            #    time.sleep(1)

    driver.quit()


if __name__ == "__main__":
    executar_downloads()
