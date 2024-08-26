import configparser
import logging
import os
import time
from datetime import datetime

import transf_producao
from database import registrar_extracao
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
    handlers=[logging.FileHandler("producao.log"), logging.StreamHandler()],
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


def executar_downloads_mes(linha, coluna, checkbox, nome_arq):
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
    falhas = 0
    for j in range(len(competencias.find_elements(By.TAG_NAME, "li"))):
        # recarregar competencias
        if j > 0:
            competencias = seleciona_competencias(driver)
        for i, competencia in enumerate(
            competencias.find_elements(By.TAG_NAME, "li")
        ):
            if i == j:
                mes = competencia.text
                # pegar o horario de inicio em timestamp
                start_time = datetime.now()

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
                if fazer_download(driver, mes, nome_arq):
                    # Recarregar a página para a próxima competência
                    driver.refresh()

                    # Registra a extração no banco de dados
                    final_time = datetime.now()
                    # Calcula o tempo de execução em segundos
                    tempo_execucao = (final_time - start_time).total_seconds()
                    # converte o tempo inicial e final para timestamp
                    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
                    final_time = final_time.strftime("%Y-%m-%d %H:%M:%S")

                    """registrar_extracao(
                        mes,
                        mes.split("/")[1],
                        "producao",
                        "Municípios",
                        nome_arq[9:],
                        nome_arq,
                        tempo_execucao,
                        start_time,
                        final_time,
                    )"""
                else:
                    falhas += 1
                    driver.quit()
                    if falhas > 3:
                        logger.error("Muitas falhas, abortando")
                        return False
                    driver = cria_driver()


    logger.info("Script Finalizado")
    # Fecha a janela do navegador
    driver.quit()


linhas = {
    "municipio": '//*[@id="selectLinha"]/optgroup[1]/option[5]',
    "competencia": '//*[@id="selectLinha"]/optgroup[1]/option[6]',
}

colunas = {
    "producao_condicao": '//*[@id="selectcoluna"]/optgroup[2]/option[3]',
    "producao_procedimento": '//*[@id="selectcoluna"]/optgroup[4]/option[1]',
    "producao_conduta": '//*[@id="selectcoluna"]/optgroup[2]/option[5]',
    "producao_aleitamento": '//*[@id="selectcoluna"]/optgroup[2]/option[1]',
    "producao_acoes": '//*[@id="selectcoluna"]/optgroup[2]/option[2]',
    "producao_vacinacao": '//*[@id="selectcoluna"]/optgroup[2]/option[4]',
    "producao_racionalidade": '//*[@id="selectcoluna"]/optgroup[2]/option[6]',
    "producao_consulta_odontologica": '//*[@id="selectcoluna"]/optgroup[3]/option[1]',
    "producao_vigilancia_bucal": '//*[@id="selectcoluna"]/optgroup[3]/option[2]',
    "producao_procedimentos_odontologicos": '//*[@id="selectcoluna"]/optgroup[3]/option[3]',
    "producao_conduta_odontologica": '//*[@id="selectcoluna"]/optgroup[3]/option[4]',
    "producao_procedimentos_pics": '//*[@id="selectcoluna"]/optgroup[4]/option[2]',
    "producao_visita": '//*[@id="selectcoluna"]/optgroup[5]/option[1]',
    "producao_desfecho_visita": '//*[@id="selectcoluna"]/optgroup[5]/option[2]',
    "producao_imovel": '//*[@id="selectcoluna"]/optgroup[5]/option[3]',
}

checkbox = {
    "producao_condicao": '//*[@id="filtrosAtendIndividual"]/div/div/div[3]/div/button',
    "producao_procedimento": '//*[@id="filtrosProcedimento"]/div/div[1]/div[1]/div/button',
    "producao_conduta": '//*[@id="filtrosAtendIndividual"]/div/div/div[5]/div/button',
    "producao_aleitamento": '//*[@id="filtrosAtendIndividual"]/div/div/div[1]/div/button',
    "producao_acoes": '//*[@id="filtrosAtendIndividual"]/div/div/div[2]/div/button',
    "producao_vacinacao": '//*[@id="filtrosAtendIndividual"]/div/div/div[4]/div/button',
    "producao_racionalidade": '//*[@id="filtrosAtendIndividual"]/div/div/div[6]/div/button',
    "producao_consulta_odontologica": '//*[@id="filtrosAtendOdontologico"]/div/div/div[1]/div/button',
    "producao_vigilancia_bucal": '//*[@id="filtrosAtendOdontologico"]/div/div/div[2]/div/button',
    "producao_procedimentos_odontologicos": '//*[@id="filtrosAtendOdontologico"]/div/div/div[3]/div/button',
    "producao_conduta_odontologica": '//*[@id="filtrosAtendOdontologico"]/div/div/div[4]/div/button',
    "producao_procedimentos_pics": '//*[@id="filtrosProcedimento"]/div/div[1]/div[2]/div/button',
    "producao_visita": '//*[@id="filtrosCondutaDesfecho"]/div/div/div[1]/div/button',
    "producao_desfecho_visita": '//*[@id="filtrosCondutaDesfecho"]/div/div/div[2]/div/button',
    "producao_imovel": '//*[@id="filtrosCondutaDesfecho"]/div/div/div[3]/div/button',
}


lista = [
    "producao_visita",
    "producao_desfecho_visita",
    "producao_imovel",
]


if __name__ == "__main__":
    for producao in lista:
        logger.info(f" -- Processando a produção {producao}  -- ")
        executar_downloads_mes(
            linhas["municipio"],
            colunas[producao],
            checkbox[producao],
            producao,
        )
        transf_producao.main()
    logger.info("Script Finalizado")
