"""Módulo para atualizar as previsões de Produção do SISAB."""

from datetime import datetime

import db
import pandas as pd
import previsao


def get_ultimos_x_meses(meses):
    """Retorna os últimos x meses."""
    consulta = f"""
    SELECT DISTINCT YEAR, MONTH FROM INDIVIDUAL_CARE
    ORDER BY YEAR DESC, MONTH DESC LIMIT {meses}
    """
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(consulta)
    meses = cur.fetchall()
    cur.close()
    conn.close()
    return meses[-1]


def get_dados(ano_mes):
    """Retorna os dados de Produção dos últimos x meses."""
    consulta = f"""
    SELECT DISTINCT ICAT.NAME, GROUP_PARAM, GU.NAME  FROM 
    INDIVIDUAL_CARE IC JOIN GEO_UNIT GU ON IC.GEO_UNIT_ID = GU.ID
    JOIN INDIVIDUAL_CARE_CATEGORY ICC ON IC.ID = ICC.INDIVIDUAL_CARE_ID
    JOIN INDIVIDUAL_CATEGORY ICAT ON ICC.INDIVIDUAL_CATEGORY_ID = ICAT.ID
    WHERE YEAR >= {ano_mes[0]} AND MONTH >= {ano_mes[1]}
    """
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(consulta)
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados


def valida_dados(dados):
    """Verifica se há dados suficientes para prever a Produção."""
    # Melhorar a validação, procurando buracos nos dados e se os últimos meses estão preenchidos
    if len(dados) < 12:
        return False
    return True


def apaga_previsao(categoria, grupo, municipio):
    """Apaga a previsão de Produção."""
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(
        f"""
        DELETE FROM INDIVIDUAL_CARE_CATEGORY_FORECASTING
        WHERE INDIVIDUAL_CARE_FORECASTING_ID IN (
            SELECT ID FROM INDIVIDUAL_CARE_FORECASTING
            WHERE GROUP_PARAM = '{grupo}'
            AND GEO_UNIT_ID IN (
                SELECT ID FROM GEO_UNIT WHERE NAME = '{municipio}'
            )
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


def insere_previsao(categoria, grupo, municipio, forecast, data):
    """Insere a previsão de Produção."""
    for i, value in enumerate(forecast):
        data = adiciona_mes(data)
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(
            f"""
        INSERT INTO INDIVIDUAL_CARE_FORECASTING (GROUP_PARAM, CLASS_PARAM, YEAR, MONTH, GEO_UNIT_ID)
        VALUES ('{grupo}', '{categoria}', {data[0]}, {data[1]}, 
        (SELECT ID FROM GEO_UNIT WHERE NAME = '{municipio}'))
        RETURNING ID
        """
        )
        id_forecasting = cur.fetchone()[0]
        cur.execute(
            f"""
            INSERT INTO INDIVIDUAL_CARE_CATEGORY_FORECASTING (VALUE, INDIVIDUAL_CARE_FORECASTING_ID, INDIVIDUAL_CATEGORY_ID)
            VALUES ({forecast[i]}, {id_forecasting}, 
            (SELECT ID FROM INDIVIDUAL_CATEGORY WHERE NAME = '{categoria}'))
            """
        )
    conn.commit()
    cur.close()
    conn.close()


def adiciona_mes(data):
    """Adiciona um mês à data."""
    if data[1] == 12:
        return (data[0] + 1, 1)
    return (data[0], data[1] + 1)


def atualiza(meses):
    """Gera combinações de grupo, categoria e município para os últimos x meses."""
    ano_mes = get_ultimos_x_meses(meses)
    combinacoes = get_dados(ano_mes)

    for combinacao in combinacoes:
        categoria = combinacao[0]
        grupo = combinacao[1]
        municipio = combinacao[2]
        dados = db.executa_query(
            db.consulta_valores(categoria, grupo, municipio)
        )
        # Concat year and month from last row
        data = (dados["year"].iloc[-1], dados["month"].iloc[-1])
        if valida_dados(dados):
            forecast = previsao.previsao_sarima(dados["value"])
            apaga_previsao(categoria, grupo, municipio)
            insere_previsao(categoria, grupo, municipio, forecast, data)
        else:
            print(
                f"Não há dados suficientes para prever {categoria} em {municipio}."
            )


# Cria a tabela caso não exista
def cria_tabelas():
    """Cria a tabela de previsão de Produção."""
    conn = db.connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS INDIVIDUAL_CARE_FORECASTING (
            ID SERIAL PRIMARY KEY,
            GROUP_PARAM VARCHAR(255),
            CLASS_PARAM VARCHAR(255),
            YEAR INTEGER,
            MONTH INTEGER,
            GEO_UNIT_ID BIGINT,
            FOREIGN KEY (GEO_UNIT_ID) REFERENCES GEO_UNIT(ID),
            CONSTRAINT unique_forecasting UNIQUE (GROUP_PARAM, CLASS_PARAM, YEAR, MONTH, GEO_UNIT_ID)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS INDIVIDUAL_CARE_CATEGORY_FORECASTING (
            ID SERIAL PRIMARY KEY,
            VALUE BIGINT,
            INDIVIDUAL_CARE_FORECASTING_ID BIGINT,
            INDIVIDUAL_CATEGORY_ID BIGINT,
            FOREIGN KEY (INDIVIDUAL_CARE_FORECASTING_ID) REFERENCES INDIVIDUAL_CARE_FORECASTING(ID),
            FOREIGN KEY (INDIVIDUAL_CATEGORY_ID) REFERENCES INDIVIDUAL_CATEGORY(ID),
            CONSTRAINT unique_value UNIQUE (INDIVIDUAL_CARE_FORECASTING_ID, INDIVIDUAL_CATEGORY_ID)
        )
        """
    )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    atualiza(3)
