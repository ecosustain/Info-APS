"""Módulo para consultar os últimos 6 meses de dados no site do SISAB e atualizar no banco de dados."""

import pandas as pd
from carregar.carregar_producao import transform_data
from extrair.extracao_producao import executar_downloads_mes, xpaths
from transformar import transf_producao


def get_meses(arquivo):
    """Função para ler o arquivo e retornar uma lista com os meses e anos."""
    arquivo = arquivo + ".csv"
    df = pd.read_csv(f"data/consolidado/{arquivo}")
    df = transform_data(df)
    meses = df["Data"].unique().tolist()
    lista = []
    # meses = [Timestamp('2024-03-01 00:00:00'), Timestamp('2024-05-01 00:00:00'), Timestamp('2024-06-01 00:00:00'), Timestamp('2024-07-01 00:00:00'), Timestamp('2024-04-01 00:00:00'), Timestamp('2024-08-01 00:00:00')]
    # Pega uma tupla de meses e anos
    for mes in meses:
        # converte de timestamp para string
        temp = str(mes)
        # pega os 7 primeiros caracteres
        temp = temp[:7]
        ano = temp[:4]
        mes_dig = temp[5:]
        lista.append((ano, mes_dig))
    return lista


def main():
    """Função principal."""
    lista = [
        "producao_profissionais_individual",
    ]

    for producao in lista:
        """executar_downloads_mes(
            xpaths["producao"][
                "municipio"
            ],  # Acessa o XPath da linha (Município)
            xpaths[producao]["coluna"],  # Acessa o XPath da coluna
            xpaths[producao]["checkbox"],  # Acessa o XPath do checkbox
            producao,
            6,
        )"""
        # transf_producao.main()
        meses = get_meses(producao)
        apaga_meses(meses, producao)


if __name__ == "__main__":
    main()

""""producao_profissionais_odontologico",
        "producao_profissionais_procedimentos",
        "producao_profissionais_visita",
        "producao_conduta_individual",
        "producao_conduta_odontologico",
        "producao_desfecho_visita","""
