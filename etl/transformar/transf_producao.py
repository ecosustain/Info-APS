"""Módulos para criar a leitura dos dados armazenados em csv."""

import os
import re
import shutil

import pandas as pd

# Carregar as configurações
transformacao_dir = os.getenv("TRANSFORMACAO_DIR", "data/transformacao")


def process_csv(file_path):
    """Função para processar o arquivo CSV e retornar um DataFrame"""
    # Ler o arquivo CSV, extraindo as 10 primeiras linhas (para pegar a linha 4)

    try:
        temp_df = pd.read_csv(
            file_path,
            nrows=10,
            thousands=".",
            header=None,
            encoding="ISO-8859-1",
        )
    except Exception as e:
        print("ERRO", file_path, e)
        raise e

    # Extrair o mês da linha 4 (index 3 porque indexação começa em 0)
    linha = (
        temp_df.iloc[3].dropna().values[0]
    )  # Supondo que o mês esteja na primeira coluna não vazia

    # Se o filepath cotains gravidas, o mês está na linha 4
    if "gravidas" in file_path:
        linha = temp_df.iloc[4].dropna().values[0]

    # Extrair o mês da linha
    mes = linha.split(" ")[1].split("/")[0]
    ano = linha.split(" ")[1].split("/")[1]

    # Ler o arquivo inteiro e remover as 7 primeiras e 4 últimas linhas
    df = pd.read_csv(
        file_path, skiprows=7, thousands=".", encoding="ISO-8859-1", sep=";"
    )  # Ignorar as 7 primeiras linhas
    df = df[:-2]  # Remover as 2 últimas linhas

    # Renomear e preencher a última coluna para mes
    df.rename(columns={df.columns[-1]: "Mes"}, inplace=True)
    df["Mes"] = mes

    # Adicionar a coluna de ano
    df["Ano"] = ano

    return df


def concat_csv_files(files):
    """Função para concatenar os arquivos CSV em grupos de 100"""
    # Inicializar um DataFrame vazio
    df = pd.DataFrame()

    # Colunas esperadas no DataFrame
    colunas = process_csv(files[0]).columns.tolist()

    # Iterar sobre os arquivos
    for i, file in enumerate(files):
        # Processar o arquivo
        try:
            temp_df = process_csv(file)
        except Exception as e:
            print("ERRO", file, e)
            print()
            continue
        # Pular arquivos que não possuem as colunas esperadas
        if temp_df.columns.tolist() != colunas:
            print(file, "não possui as colunas esperadas")
            print("Colunas DF", temp_df.columns.tolist())
            print()
            continue
        # Concatenar com o DataFrame principal
        df = pd.concat([df, temp_df])

        # Salvar a cada 100 arquivos
        if i % 100 == 0 and i > 0:
            df.to_csv(f"partial_{i}.csv", index=False)
            df = pd.DataFrame()
    # Salvar o restante
    df.to_csv(f"partial_{i}.csv", index=False)


# Função para listar os arquivos CSV
def list_files(directory="."):
    """Função para listar os arquivos CSV em um diretório"""

    # Listar os arquivos com o diretório
    files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".csv")
    ]

    return files


def remove_trailing_dot_zero(value):
    """Função para remover o .0 no final do número"""
    # Substitui apenas se o valor termina com ".0"
    return re.sub(r"\.0$", "", value)


def concat_final_csv(name, diretorio="."):
    """Função para concatenar os arquivos CSV"""
    # Inicializar um DataFrame vazio
    df = pd.DataFrame()
    for file in list_files(diretorio):
        df_temp = pd.read_csv(file, dtype=str, thousands=".")
        df = pd.concat([df, df_temp])
    # Remove duplicados
    df.drop_duplicates(inplace=True)
    df = df.map(remove_trailing_dot_zero)
    # Remover ponto dos anos e transformar em inteiro
    df["Ano"] = df["Ano"].str.replace(".", "").astype(int)

    # Salvar o arquivo final
    df.to_csv(f"{name}.csv", index=False)
    return df


def remove_temp_files(transf_dir):
    """Função para remover os arquivos temporários"""
    for file in os.listdir("."):
        if file.startswith("partial_"):
            os.remove(file)
    for file in os.listdir(transf_dir):
        if file.endswith(".csv"):
            os.remove(os.path.join(transf_dir, file))


def main():
    """Função principal"""
    print("Iniciando a transformação dos dados")
    # Listar os arquivos
    files = list_files(transformacao_dir)
    # Pega o nome do arquivo sem a data
    nome_arq = files[0][:-13]
    print("Concatenando os arquivos")
    # Concatenar os arquivos
    concat_csv_files(files)
    print("Concatenando o arquivo final")
    # Concatenar o arquivo final
    nome_arq = nome_arq.split("/")[-1]
    df = concat_final_csv(nome_arq)
    print("Removendo os arquivos temporários")
    if len(df) > 1000:
        remove_temp_files(transformacao_dir)
        # Copiar o arquivo final para o volume compartilhado
        shutil.copy(f"{nome_arq}.csv", f"/shared_data/{nome_arq}.csv")
        os.remove(f"{nome_arq}.csv")
        print("Transformação concluída")
    else:
        print("Erro na transformação")


if __name__ == "__main__":
    main()
