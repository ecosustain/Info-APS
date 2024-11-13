"""Fluxo principal do ETL."""

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
lista = [
    "producao_profissionais_individual",
    "producao_conduta",
    "producao_condicao",
    "producao_tipo",
]

if __name__ == "__main__":
    # Número de meses de download
    N_MONTHS = 1000
    logger.info(" -- Iniciando a extracao Cadastros  -- ")
    extracao_cadastros.download_cadastro(N_MONTHS)
    transformacao.main("cadastro")
    logger.info(" -- Iniciando a extracao Codigos  -- ")
    extracao_codigos.extrair_codigos(N_MONTHS)
    transf_producao.main()
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
    logger.info(" -- Iniciando a extracao Gravidas  -- ")
    extracao_gravidas.executar_downloads_mes(
        xpaths["gravidas"]["municipio"],
        xpaths["gravidas"]["coluna"],
        "gravidas",
        N_MONTHS,
    )
    transf_producao.main()
