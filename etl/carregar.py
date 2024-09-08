import time

import pandas as pd
import psycopg2.extras as extras
from database import conectar_db


def converter_mes(mes):
    """Função para converter o mês de string para número."""
    meses = {
        "JAN": 1,
        "FEV": 2,
        "MAR": 3,
        "ABR": 4,
        "MAI": 5,
        "JUN": 6,
        "JUL": 7,
        "AGO": 8,
        "SET": 9,
        "OUT": 10,
        "NOV": 11,
        "DEZ": 12,
    }

    return meses.get(mes.upper(), 1)


# Função para transformar dados (ex.: combinar mês e ano em uma data)
def transform_data(df):
    """Função para criar a coluna de data."""
    # Converter o mes
    df["Mes"] = df["Mes"].apply(converter_mes)
    # Criar uma nova coluna de data no formato adequado
    df["Data"] = pd.to_datetime(
        df["Ano"].astype(str) + "-" + df["Mes"].astype(str) + "-01"
    )
    # Remover colunas 'Mes' e 'Ano'
    df = df.drop(columns=["Mes", "Ano"])
    return df


def ajusta_producao(df):
    """Ajusta o DataFrame de produção."""
    df["Uf"] = df["Uf"].str.upper()
    # Para as colunas que não sejam Uf, Municipio e mes
    try:
        for col in df.columns.difference(["Uf", "Municipio", "Mes"]):
            df[col] = (
                pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            )
    except Exception as e:
        print(f"Erro ao converter a coluna {col} para inteiro: {e}")

    return df


def valida_producao(df):
    """Valida os dados de produção."""
    # Verifica se possui nulos
    if df.isnull().values.any():
        raise ValueError("Existem valores nulos no DataFrame.")
    # Verifica se os tipos estão corretos


def ler_producao(nome_arq):
    """Lê o arquivo de produção."""
    return pd.read_csv(nome_arq, sep=",", encoding="utf-8")


def cadastra_tipo_atendimento(tipo_atendimento):
    """Cadastra o tipo de atendimento no banco de dados."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tipo_atendimento (descricao) VALUES (%s)",
        (tipo_atendimento,),
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Tipo de atendimento {tipo_atendimento} cadastrado com sucesso.")


def cadastra_grupo(grupo, tipo_atendimento):
    """Cadastra o grupo no banco de dados."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO grupo_filtros (descricao, tipo_atendimento_id) VALUES (%s, %s)",
        (grupo, tipo_atendimento),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_id_tipo_atendimento(tipo_atendimento):
    """Retorna o id do tipo de atendimento."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM tipo_atendimento WHERE descricao = %s",
        (tipo_atendimento,),
    )
    id_tipo_atendimento = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return id_tipo_atendimento


def get_id_grupo(grupo, id_tipo_atendimento):
    """Retorna o id do grupo."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM grupo_filtros WHERE descricao = %s and tipo_atendimento_id = %s",
        (grupo, id_tipo_atendimento),
    )
    id_grupo = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return id_grupo


def valida_tipo_atendimento_bd(tipo_atendimento):
    """Verifica se o tipo de atendimento está cadastrado no banco de dados."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tipo_atendimento")
    tipos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not any(tipo_atendimento == tipo[1] for tipo in tipos):
        print("Atendimento não cadastrado no banco de dados.")
        cadastra_tipo_atendimento(tipo_atendimento)
        id_atendimento = get_id_tipo_atendimento(tipo_atendimento)
    else:
        # Pegar o id do tipo de atendimento
        id_atendimento = [
            tipo[0] for tipo in tipos if tipo[1] == tipo_atendimento
        ][0]

    return id_atendimento


def valida_grupos_bd(id_atendimento, grupo):
    """Verifica se o banco de dados possui a hierarquia correta."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grupo_filtros")
    grupos = cursor.fetchall()
    if not any((grupo == g[1] and id_atendimento == g[2]) for g in grupos):
        print("Grupo não cadastrado no banco de dados.")
        cadastra_grupo(grupo, id_atendimento)
        id_grupo = get_id_grupo(grupo, id_atendimento)
    else:
        # Pegar o id do grupo
        id_grupo = [
            g[0] for g in grupos if (grupo == g[1] and id_atendimento == g[2])
        ][0]
    cursor.close()
    conn.close()

    return id_grupo


def valida_colunas_bd(df, id_grupo):
    """Valida se as colunas do DataFrame estão registradas no banco de dados."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM filtros WHERE grupo_filtro_id = %s", (id_grupo,)
    )
    colunas = cursor.fetchall()
    for col in df.columns.difference(
        ["Uf", "Municipio", "Mes", "Ibge", "Data"]
    ):
        if not any(col == c[1] for c in colunas):
            print(f"Coluna {col} não cadastrada no banco de dados.")
            cursor.execute(
                "INSERT INTO filtros (grupo_filtro_id, descricao) VALUES (%s, %s)",
                (id_grupo, col),
            )
    # Cria um dicionário com as colunas e seus respectivos ids
    dict_colunas = {}
    for col in df.columns.difference(
        ["Uf", "Municipio", "Mes", "Ibge", "Data"]
    ):
        for c in colunas:
            if col == c[1]:
                dict_colunas[col] = c[0]
                break
    conn.commit()
    cursor.close()
    conn.close()
    return dict_colunas


def carrega_banco(df, colunas):
    """Carrega os dados de produção no banco de dados."""
    conn = conectar_db()
    cursor = conn.cursor()
    start_time = time.time()

    # Prepara a lista de tuplas para inserção em massa
    dados = []
    for i, row in df.iterrows():
        for col in colunas:
            dados.append((colunas[col], row["Ibge"], row["Data"], row[col]))

    # Usa executemany para inserir múltiplas linhas de uma vez
    query = """
    INSERT INTO filtro_producao (filtro_id, ibge, data, valor)
    VALUES (%s, %s, %s, %s)
    """

    try:
        # Executa a inserção em massa
        extras.execute_batch(cursor, query, dados, page_size=1000)

        # Commit das alterações
        conn.commit()
        print("Dados carregados com sucesso.")

    except Exception as e:
        # Rollback em caso de erro
        conn.rollback()
        print(f"Erro ao carregar dados: {e}")

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        elapsed_time = time.time() - start_time
        print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

    return "Processo concluído."


def ajusta_coluna(df):
    """Ajusta a coluna."""
    for col in df.columns.difference(
        ["Uf", "Municipio", "Mes", "Ibge", "Data"]
    ):
        # Rename columns
        if "Individual" in col:
            df.rename(columns={col: "Individual"}, inplace=True)
        elif "Procedimento" in col:
            df.rename(columns={col: "Procedimento"}, inplace=True)
        elif "Visita" in col:
            df.rename(columns={col: "Visita"}, inplace=True)
        elif "Odontológico" in col:
            df.rename(columns={col: "Odontológico"}, inplace=True)
    return df


def tipo_atendimento(df):
    """Carrega os arquivos dos totais de produção."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tipo_atendimento")
    colunas = cursor.fetchall()
    tipo_producao = {}
    for col in df.columns.difference(
        ["Uf", "Municipio", "Mes", "Ibge", "Data"]
    ):
        for c in colunas:
            if col in c[1]:
                tipo_producao[col] = c[0]
    return tipo_producao


def tipo_producao(df):
    """Carrega os arquivos dos totais de produção."""
    df = ajusta_coluna(df)
    tipo_producao = tipo_atendimento(df)
    for tipo in tipo_producao:
        tipo_producao[tipo] = [
            tipo_producao[tipo],
            valida_grupos_bd(tipo_producao[tipo], "Total"),
        ]
    for tipo in tipo_producao:
        tipo_producao[tipo].append(
            valida_colunas_bd(df, tipo_producao[tipo][1])
        )

    conn = conectar_db()
    cursor = conn.cursor()
    start_time = time.time()

    # Prepara a lista de tuplas para inserção em massa
    dados = []
    for i, row in df.iterrows():
        for col in tipo_producao:
            dados.append(
                (
                    tipo_producao[col][2][col],
                    row["Ibge"],
                    row["Data"],
                    row[col],
                )
            )

    # Usa executemany para inserir múltiplas linhas de uma vez
    query = """
    INSERT INTO filtro_producao (filtro_id, ibge, data, valor)
    VALUES (%s, %s, %s, %s)
    """

    try:
        # Executa a inserção em massa
        # extras.execute_batch(cursor, query, dados, page_size=1000)

        # Commit das alterações
        # conn.commit()
        # print("Dados carregados com sucesso.")
        print(dados)
    except Exception as e:
        # Rollback em caso de erro
        conn.rollback()
        print(f"Erro ao carregar dados: {e}")

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

        elapsed_time = time.time() - start_time
        print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

    return "Processo concluído."
