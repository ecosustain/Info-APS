"""Módulo com funções auxiliares para o painel"""

import geopandas as gpd
import pandas as pd


def get_columns():
    """Função para retornar as colunas do DataFrame"""
    colunas = {
        "Problemas": [
            "Asma",
            "Desnutrição",
            "Diabetes",
            "DPOC",
            "Hipertensão arterial",
            "Obesidade",
            "Pré-natal",
            "Puericultura",
            "Puerpério (até 42 dias)",
            "Saúde sexual e reprodutiva",
            "Tabagismo",
            "Usuário de álcool",
            "Usuário de outras drogas",
            "Saúde mental",
            "Reabilitação",
            "D.Transmissíveis - Dengue",
            "Doenças transmissíveis - DST",
            "D.Transmissíveis - Hanseníase",
            "D.Transmissíveis - Tuberculose",
            "Rast. câncer de mama",
            "Rast. câncer do colo do útero",
            "Rast. risco cardiovascular",
        ],
        "Condutas Odontológicas": [
            "Agendamento p/ grupos",
            "Agendamento p/ outros profissi",
            "Encaminhamento - Cirurgia BMF",
            "Encaminhamento - Endodontia",
            "Encaminhamento - Estomatologia",
            "Encaminhamento - Implantodonti",
            "Encaminhamento - Odontopediatr",
            "Encaminhamento - Ortodontia/Or",
            "Encaminhamento - Outros",
            "Encaminhamento - Pacientes com",
            "Encaminhamento - Periodontia",
            "Encaminhamento - Prótese dentá",
            "Encaminhamento - Radiologia",
        ],
        "Condutas": [
            "Agendamento para grupos",
            "Encaminhamento interno no dia",
            "Encaminhamento intersetorial",
            "Encaminhamento p/ CAPS",
            "Encaminhamento p/ internação h",
            "Encaminhamento p/ serviço de a",
            "Encaminhamento p/ serviço espe",
            "Encaminhamento p/ urgência",
        ],
        "Procedimentos": [
            "Acuputura - ins. de agulhas",
            "Adm.  med. via endovenosa",
            "Adm.  med. via intramuscular",
            "Adm. Med. inalação/nebulização",
            "Adm. Med. via tópica",
            "Adm. med. via Subcutânea (SC)",
            "Adm. med. via oral",
            "Adm. penicilina p/ tto sífilis",
            "Caut. química pequenas lesões",
            "Cir. de unha (cantoplastia)",
            "Col. de cito. De colo uterino",
            "Col. mat. p/ ex. laboratorial",
            "Exérese/biopsia/punção de tum.",
            "Fundoscopia",
            "Infiltração em cav. sinovial",
            "Rem. Corp. Estranho Subcutâneo",
            "Rm. C. Est. Cav Auditiva/Nasal",
            "TERAPIA DE REIDRATACAO ORAL",
            "Tes. Ráp. p/ dosg. proteinúria",
        ],
        "Motivo Visita": [
            "Acomp.  Domiciliados/Acamados",
            "Acomp.  Pessoa c/ Diabetes",
            "Acomp.  Pessoa c/ Hanseníase",
            "Acomp.  Pessoa c/ Tuberculose",
            "Acomp.  Pessoas c/ D. Crônicas",
            "Acomp.  Recém-nascido",
            "Acomp. -  DPOC/Enfisema",
            "Acomp. - Usuário de drogas",
            "Acomp. Cond.  Bolsa Família",
            "Acomp. Condições de V.S.",
            "Acomp. PCD  ou reabilitação",
            "Acomp. Pessoa c/ Asma",
            "Acomp. Pessoa c/ Câncer",
            "Acomp. Pessoa c/ Desnutrição",
            "Acomp. Pessoa c/ Hipertensão",
            "Acomp. Sintomáticos Resp.",
            "Acomp. Usuário de álcool",
            "Acompanhamento - Criança",
            "Acompanhamento - Gestante",
            "Acompanhamento - Puérpera",
            "Acompanhamento - Saúde mental",
            "Acompanhamento - Tabagista",
            "B.A. - Cond.  Bolsa Família",
            "Busca ativa - Consulta",
            "Busca ativa - Exame",
            "Cadastramento/Atualização",
            "Controle de Ambientes/Vetores",
            "Convite At.Col./Camp. Saúde",
            "Egresso de Internação",
            "Outros",
        ],
    }

    return colunas


def normaliza(df, populacao):
    """Agrupa os dados por município e normaliza os casos por 100.000 habitantes"""
    # Mesclar o DataFrame original com o DataFrame de população
    df = pd.merge(df, populacao[["Ibge", "populacao"]], on="Ibge")

    # Selecionar colunas de casos (excluindo as colunas não numéricas e a população)
    casos = df.drop(
        columns=["Ano", "Mes", "Municipio", "Uf", "Data", "Ibge", "populacao"]
    )

    # Normalizar os casos pela população do município e multiplicar por 100.000
    df_normalizado = casos.div(df["populacao"], axis=0) * 100000

    # Re-adicionar as colunas que foram removidas
    df_normalizado["Data"] = df["Data"]
    df_normalizado["Municipio"] = df["Municipio"]
    df_normalizado["Uf"] = df["Uf"]
    df_normalizado["Ibge"] = df["Ibge"]
    df_normalizado["populacao"] = df["populacao"]

    # Reordenar as colunas para manter a mesma ordem que o DataFrame original
    df_normalizado = df_normalizado[
        ["Data", "Municipio", "Uf", "Ibge", "populacao"] + list(casos.columns)
    ]

    return df_normalizado


def normaliza_por_estado(df, populacao):
    """Agrupa os dados por estado e normaliza os casos por 100.000 habitantes"""
    # renomear coluna 'UF' para 'Uf'
    populacao.rename(columns={"uf": "Uf"}, inplace=True)

    df = pd.merge(df, populacao[["Ibge", "populacao"]], on="Ibge")

    # Agrupar população por estado
    populacao_estado = populacao.groupby("Uf")["populacao"].sum().reset_index()

    # Mesclar o DataFrame original com o DataFrame de população por estado
    df = pd.merge(df, populacao_estado, on="Uf", suffixes=("", "_estado"))

    # Selecionar colunas de casos (excluindo as colunas não numéricas e a população)
    casos = df.drop(
        columns=[
            "Ano",
            "Mes",
            "Municipio",
            "Uf",
            "Data",
            "Ibge",
            "populacao",
            "populacao_estado",
        ]
    )

    # Normalizar os casos pela população total do estado e multiplicar por 100.000
    df_normalizado = casos.div(df["populacao_estado"], axis=0) * 100000

    # Re-adicionar as colunas que foram removidas
    df_normalizado["Data"] = df["Data"]
    df_normalizado["Municipio"] = df["Municipio"]
    df_normalizado["Uf"] = df["Uf"]
    df_normalizado["Ibge"] = df["Ibge"]
    df_normalizado["populacao_estado"] = df["populacao_estado"]

    # Reordenar as colunas para manter a mesma ordem que o DataFrame original
    df_normalizado = df_normalizado[
        ["Data", "Municipio", "Uf", "Ibge", "populacao_estado"]
        + list(casos.columns)
    ]

    return df_normalizado


def cria_mapa_uf(df_norm_uf, data_inicio, data_fim):
    """Cria um mapa com os dados normalizados por estado"""
    # Carregar o shapefile dos estados do Brasil (arquivo baixado shapefile do IBGE 2022)
    shapefile_uf = "../mapas/BR_UF_2022/BR_UF_2022.shp"
    brasil_estados = gpd.read_file(shapefile_uf)

    df_norm_uf = (
        df_norm_uf[
            (df_norm_uf["Data"] >= data_inicio)
            & (df_norm_uf["Data"] <= data_fim)
        ]
        .groupby("Uf")
        .sum()
        .reset_index()
    )
    df_norm_uf.drop(
        columns=["Data", "Municipio", "Ibge", "populacao_estado"], inplace=True
    )

    # Juntar os dados com o shapefile
    mapa_uf = brasil_estados.merge(
        df_norm_uf, left_on="SIGLA_UF", right_on="Uf"
    )

    # Simplificar a geometria (ajuste o parâmetro 'tolerance' conforme necessário)
    mapa_uf["geometry"] = mapa_uf["geometry"].simplify(tolerance=0.1)

    return mapa_uf


def get_producao():
    """Função para carregar o DataFrame de produção"""
    # Carregar o arquivo CSV
    df = pd.read_csv("data/producao.csv")

    return df


def get_populacao():
    """Função para carregar o DataFrame de população"""
    # Carregar o arquivo CSV
    df = pd.read_csv("data/populacao.csv")

    return df


populacao = get_populacao()
producao = get_producao()

df_normalizado = normaliza(producao, populacao)
df_norm_uf = normaliza_por_estado(producao, populacao)
