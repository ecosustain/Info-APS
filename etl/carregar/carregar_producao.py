"""Módulo para carregar os dados de produção no banco de dados."""
import pandas as pd
from carregar.carregar import (
    ajusta_producao,
    carrega_banco,
    ler_producao,
    tipo_producao,
    transform_data,
    valida_colunas_bd,
    valida_grupos_bd,
    valida_producao,
    valida_tipo_atendimento_bd,
)
from extrair.extracao import carregar_xpaths


def main(arquivo):
    """Função principal."""

    xpaths = carregar_xpaths()

    nome_arq = arquivo + ".csv"
    xpath = xpaths[arquivo]
    tipo_atendimento = xpath["tipo_atendimento"]
    grupo = xpath["grupo"]

    df = ler_producao(f"data/consolidado/{nome_arq}")
    df = ajusta_producao(df)
    print("DataFrame ajustado")
    valida_producao(df)
    print("DataFrame validado")
    df = transform_data(df)
    if tipo_atendimento == "Todos":
        return tipo_producao(df)
    id_atendimento = valida_tipo_atendimento_bd(tipo_atendimento)
    id_grupo = valida_grupos_bd(id_atendimento, grupo)
    colunas = valida_colunas_bd(df, id_grupo)
    print("Hierarquia no BD validada")
    carrega_banco(df, colunas)


if __name__ == "__main__":
    lista = ["producao_tipo"]

    for item in lista:
        main(item)


"""
Arquivos solicitados

1. Atendimentos individuais por profissional
2. Atendimentos odontológicos por profissional
3. Procedimentos por profissional
4. Visita domiciliar por profissional
5. Atendimentos individuais por conduta
6. Atendimentos odontológicos por conduta
7. Visita domiciliar por desfecho
'producao_profissionais_individual',
'producao_profissionais_odontologico',
'producao_profissionais_procedimentos',
'producao_profissionais_visita',
'producao_desfecho_visita',
"""
