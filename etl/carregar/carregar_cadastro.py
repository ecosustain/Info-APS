import pandas as pd
from database import conectar_db

from etl.carregar.carregar import transform_data


# Função para validar os dados do CSV
def validar_cadastro(df):
    required_columns = ["Uf", "IBGE", "Municipio", "Cadastros", "Mes", "Ano"]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")
    # Verificar se a coluna 'Cadastros' é numérica
    if df["Cadastros"].dtype != "int64":
        raise ValueError("Column 'Cadastros' must be numeric.")
    # Verificar se a coluna 'Mes' é uma string
    if df["Mes"].dtype != "object":
        raise ValueError("Column 'Mes' must be a string.")
    # Verificar se a coluna 'Ano' é numérica
    if df["Ano"].dtype != "int64":
        raise ValueError("Column 'Ano' must be numeric.")
    # Verificar se a coluna 'IBGE' é numérica
    if df["IBGE"].dtype != "int64":
        raise ValueError("Column 'IBGE' must be numeric.")
    # Verificar se a coluna 'Uf' é uma string
    if df["Uf"].dtype != "object":
        raise ValueError("Column 'Uf' must be a string.")
    # Verificar se a coluna 'Municipio' é uma string
    if df["Municipio"].dtype != "object":
        raise ValueError("Column 'Municipio' must be a string.")
    # Verificar se a coluna 'Mes' contém apenas valores válidos
    if (
        not df["Mes"]
        .str.upper()
        .isin(
            [
                "JAN",
                "FEV",
                "MAR",
                "ABR",
                "MAI",
                "JUN",
                "JUL",
                "AGO",
                "SET",
                "OUT",
                "NOV",
                "DEZ",
            ]
        )
        .all()
    ):
        raise ValueError("Invalid values in column 'Mes'.")
    # Verificar se a coluna 'Uf' contém apenas valores válidos
    if (
        not df["Uf"]
        .str.upper()
        .isin(
            [
                "AC",
                "AL",
                "AP",
                "AM",
                "BA",
                "CE",
                "DF",
                "ES",
                "GO",
                "MA",
                "MT",
                "MS",
                "MG",
                "PA",
                "PB",
                "PR",
                "PE",
                "PI",
                "RJ",
                "RN",
                "RS",
                "RO",
                "RR",
                "SC",
                "SP",
                "SE",
                "TO",
            ]
        )
        .all()
    ):
        raise ValueError("Invalid values in column 'Uf'.")
    # Verificar se a coluna 'Cadastros' contém apenas valores positivos
    if (df["Cadastros"] < 0).any():
        raise ValueError(
            "Column 'Cadastros' must contain only positive values."
        )
    # Verificar se a coluna 'Ano' contém apenas valores válidos
    if (df["Ano"] < 2000).any():
        raise ValueError("Column 'Ano' must contain only valid values.")
    # Verificar se algum valor é nulo
    if df.isnull().values.any():
        raise ValueError("Null values are not allowed.")


# Função para carregar os dados no banco
def load_data_to_db(df):
    """Função para carregar os dados no banco de dados."""
    conn = conectar_db()
    cursor = conn.cursor()

    # Query de inserção no banco
    insert_query = """
    INSERT INTO cadastros (ibge, data, cadastros)
    VALUES (%s, %s, %s)
    ON CONFLICT (ibge, data) DO UPDATE SET
    cadastros = EXCLUDED.cadastros;
    """

    # Percorrer cada linha do dataframe e inserir no banco
    for _, row in df.iterrows():
        cursor.execute(
            insert_query, (row["IBGE"], row["Data"], row["Cadastros"])
        )

    # Commit para garantir que as alterações sejam persistidas
    conn.commit()
    cursor.close()
    conn.close()


# Função principal do script
def main():
    """Função principal para carregar os dados."""
    try:
        # Carregar os dados do CSV
        df = pd.read_csv("data/consolidado/Cadastro.csv")

        # Validar os dados
        validar_cadastro(df)

        # Transformar os dados (ex.: criar a coluna de data)
        df = transform_data(df)

        # Carregar os dados no banco
        load_data_to_db(df)

        print("Dados carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")


if __name__ == "__main__":
    main()
