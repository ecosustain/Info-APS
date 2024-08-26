from datetime import datetime

import psycopg2
from psycopg2 import sql


def conectar_db():
    """Conecta ao banco de dados PostgreSQL local."""
    try:
        conn = psycopg2.connect(
            dbname="extracoes_db",  # Substitua pelo nome do seu banco de dados
            user="postgres",  # Substitua pelo usuário do banco de dados
            password="saude_basica_pwd",  # Substitua pela senha do banco de dados
            host="127.0.0.1",  # Substitua pelo host, se necessário
            port="5432",  # Porta padrão do PostgreSQL
        )
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def criar_tabela_extracoes():
    """Cria a tabela de extracoes no banco de dados, se não existir."""
    conn = conectar_db()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS extracoes (
                    id SERIAL PRIMARY KEY,
                    mes TEXT,
                    ano TEXT,
                    tipo_relatorio TEXT,
                    linha TEXT,
                    coluna TEXT,
                    nome_arq TEXT,
                    tempo_execucao REAL,
                    inicio TIMESTAMP,
                    fim TIMESTAMP
                );
            """
            )
            conn.commit()
    except psycopg2.DatabaseError as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        conn.close()


def registrar_extracao(
    mes,
    ano,
    tipo_relatorio,
    linha,
    coluna,
    nome_arq,
    tempo_execucao,
    inicio,
    fim,
):
    """Insere um novo registro na tabela extracoes."""
    conn = conectar_db()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO extracoes (mes, ano, tipo_relatorio, linha, coluna, nome_arq, tempo_execucao, inicio, fim)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
                (
                    mes,
                    ano,
                    tipo_relatorio,
                    linha,
                    coluna,
                    nome_arq,
                    tempo_execucao,
                    inicio,
                    fim,
                ),
            )
            conn.commit()
    except psycopg2.DatabaseError as e:
        print(f"Erro ao inserir registro: {e}")
    finally:
        conn.close()
