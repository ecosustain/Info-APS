"""Módulo para se conectar ao banco de dados local postgresql."""

import pandas as pd
import psycopg2


# Cria a conexão com o banco de dados
def connect():
    """Cria a conexão com o banco de dados."""
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="saude_basica_development",
        user="saude_basica",
        password="saude_basica",
    )
    return conn


def consulta_valores(categoria, grupo, municipio):
    """Cria a query de consulta ao banco de dados."""
    query = f"""
    SELECT VALUE, YEAR, MONTH FROM INDIVIDUAL_CARE_CATEGORY JOIN 
    (SELECT ID, YEAR, MONTH FROM INDIVIDUAL_CARE WHERE GROUP_PARAM ='{grupo}' AND GEO_UNIT_ID IN (
	SELECT ID FROM GEO_UNIT WHERE TYPE_ID = 'Municipio' AND NAME = '{municipio}')) AS INDIVIDUAL_CARE 
	ON INDIVIDUAL_CARE.ID = INDIVIDUAL_CARE_CATEGORY.INDIVIDUAL_CARE_ID 
	WHERE INDIVIDUAL_CATEGORY_ID IN (SELECT ID FROM INDIVIDUAL_CATEGORY WHERE NAME = '{categoria}')
    """
    return query


# query = consulta_valores('Atendimento Individual', 'Tipo Produção', 'SÃO PAULO')


def executa_query(query):
    """Executa a query no banco de dados."""
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    # cria um dataframe com os dados da query
    dados = pd.DataFrame(cur.fetchall(), columns=["value", "year", "month"])
    cur.close()
    conn.close()
    # ordenar os dados por ano e mes
    dados = dados.sort_values(by=["year", "month"])
    # Reindex
    dados = dados.reset_index(drop=True)
    return dados
