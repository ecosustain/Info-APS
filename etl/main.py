"""Fluxo principal do ETL."""

import os

from extrair import (
    extracao_cadastros,
    extracao_codigos,
    extracao_gravidas,
    extracao_producao,
)
from extrair.extracao import carregar_xpaths, get_logger
from transformar import transf_producao, transformacao

logger = get_logger("main.log")
xpaths = carregar_xpaths()

# Lista de arquivos de producao
lista_site = [
    "producao_profissionais_individual",
    "producao_conduta",
    "producao_condicao",
    "producao_tipo",
]

lista_extras = [
    "producao_procedimento",
    "producao_procedimentos_odontologicos",
    "producao_aleitamento",
    "producao_vacinacao",
    "producao_acoes",
    "producao_racionalidade",
    "producao_consulta_odontologica",
    "producao_vigilancia_bucal",
    "producao_conduta_odontologica",
    "producao_visita",
    "producao_desfecho_visita",
    "producao_imovel",
    "producao_profissionais_odontologico",
    "producao_profissionais_procedimentos",
    "producao_profissionais_visita",
]


def limpa_diretorios():
    """Função para limpar os diretórios de downloads."""
    down_dir = os.getenv("DOWNLOAD_DIR", "data/download")
    transf_dir = os.getenv("TRANSFORM_DIR", "data/transformacao")
    logger.info(" -- Limpando diretórios  -- ")
    os.system(f"rm -rf {down_dir}/*")
    os.system(f"rm -rf {transf_dir}/*")


def loop_lista(lista, N_MONTHS):
    """Função para executar o loop da lista de arquivos."""
    for producao in lista:
        logger.info(f" -- Iniciando a extracao {producao}  -- ")
        extracao_producao.executar_downloads_mes(
            xpaths["producao"][
                "municipio"
            ],  # Acessa o XPath da linha (Município)
            xpaths[producao]["coluna"],  # Acessa o XPath da coluna
            xpaths[producao]["checkbox"],  # Acessa o XPath do checkbox
            producao,
            N_MONTHS,
        )
        transf_producao.main()


if __name__ == "__main__":
    # Número de meses de download
    N_MONTHS = 3
    limpa_diretorios()
    logger.info(" -- Iniciando a extracao Cadastros  -- ")
    extracao_cadastros.download_cadastro(N_MONTHS)
    transformacao.main("cadastro")
    logger.info(" -- Iniciando a extracao Codigos  -- ")
    extracao_codigos.extrair_codigos(N_MONTHS)
    transf_producao.main()
    # Loop para os arquivos do site
    loop_lista(lista_site, N_MONTHS)
    logger.info(" -- Iniciando a extracao Gravidas  -- ")
    extracao_gravidas.executar_downloads_mes(
        xpaths["gravidas"]["municipio"],
        xpaths["gravidas"]["coluna"],
        "gravidas",
        N_MONTHS,
    )
    transf_producao.main()
    # Loop para os arquivos extras
    loop_lista(lista_extras, N_MONTHS)
