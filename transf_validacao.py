# código para criar a leitura dos dados armazenados em csv
import configparser
import itertools
import os
from datetime import datetime

import pandas as pd

# Carregar o arquivo de configuração
config = configparser.ConfigParser()
config.read("config.ini")

transformacao_dir = config["Paths"]["transformacao_dir"]


def process_csv(file_path):
    """Função para processar o arquivo CSV e retornar um DataFrame"""
    # Ler o arquivo CSV, extraindo as 10 primeiras linhas (para pegar a linha 4)
    temp_df = pd.read_csv(file_path, nrows=10, header=None, encoding="ISO-8859-1")

    # Extrair o mês da linha 4 (index 3 porque indexação começa em 0)
    linha = (
        temp_df.iloc[3].dropna().values[0]
    )  # Supondo que o mês esteja na primeira coluna não vazia

    # Extrair o mês da linha
    mes = linha.split(" ")[1].split("/")[0]
    ano = linha.split(" ")[1].split("/")[1]

    # Ler o arquivo inteiro e remover as 7 primeiras e 4 últimas linhas
    df = pd.read_csv(
        file_path, skiprows=7, encoding="ISO-8859-1", sep=";"
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
    colunas = [
        "Região",
        "Uf",
        "IBGE",
        "Municipio",
        "CNES",
        "Tipo Unidade",
        "INE",
        "Tipo Equipe",
        "Validação",
        "Total",
        "Mes",
        "Ano",
    ]

    # Iterar sobre os arquivos
    for i, file in enumerate(files):
        # Processar o arquivo
        temp_df = process_csv(file)

        # Pular arquivos que não possuem as colunas esperadas
        if temp_df.columns.tolist() != colunas:
            print(file, "não possui as colunas esperadas")
            continue
        # Concatenar com o DataFrame principal
        df = pd.concat([df, temp_df])

        # Salvar a cada 100 arquivos
        if i % 100 == 0 and i > 0:
            df.to_csv(f"data_{i}.csv", index=False)
            df = pd.DataFrame()

    df.to_csv(f"data_{i}.csv", index=False)


# Função para listar os arquivos CSV
def list_files(directory="/home/daniel/Downloads"):
    """Função para listar os arquivos CSV em um diretório"""
    import os

    # Listar os arquivos com o diretório
    files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".csv")
    ]

    return files


def concat_final_csv(dir="."):    
    """Função para concatenar os arquivos CSV"""
    # Inicializar um DataFrame vazio
    df = pd.DataFrame()
    for file in list_files(dir):
        df_temp = pd.read_csv(file)
        df = pd.concat([df, df_temp])
    # Remove duplicados
    df.drop_duplicates(inplace=True)
    # Salvar o arquivo final
    df.to_csv("data.csv", index=False)
    return df


def ausentes(df):
    """Função para contar os valores ausentes em um DataFrame"""

    now = datetime.now()
    ano_atual = now.year + 1
    mes_atual = now.month + 1

    anos = list(range(2021, ano_atual))
    mes = list(range(1, mes_atual))

    combinacoes = list(itertools.product(df['Uf'].unique(), df['Mes'].unique(), anos))
    combinacoes_24 = list(itertools.product(df['Uf'].unique(), mes, [2024]))

    combinacoes = combinacoes + combinacoes_24

    # Filtrar as combinações que já existem no DataFrame
    combinacoes_existentes = set(zip(df['Uf'], df['Mes'], df['Ano']))

    # Identificar as combinações ausentes
    combinacoes_ausentes = [comb for comb in combinacoes if comb not in combinacoes_existentes]
    return combinacoes_ausentes


def existentes(df):
    """Função para contar os valores existentes em um DataFrame"""

    # Filtrar as combinações que já existem no DataFrame
    combinacoes_existentes = set(zip(df['Uf'], df['Mes'], df['Ano']))

    return combinacoes_existentes


def atualiza_controle(combinacoes_existentes):
    """Função para atualizar o controle de combinações"""
    with open('controle_validacao.txt', 'w') as f:
        for comb in combinacoes_existentes:
            if comb[1] < 10:
                f.write(f'{comb[0]}_0{comb[1]}/{comb[2]}\n')
            else:
                f.write(f'{comb[0]}_{comb[1]}/{comb[2]}\n')


def remove_temp_files(transformacao_dir):
    """Função para remover os arquivos temporários"""
    for file in os.listdir("."):
        if file.startswith("data_"):
            os.remove(file)
    for file in os.listdir(transformacao_dir):
        if file.endswith(".csv"):
            os.remove(os.path.join(transformacao_dir, file))


if __name__ == "__main__":
    print("Iniciando a transformação dos dados")
    # Listar os arquivos
    files = list_files(transformacao_dir)
    print("Concatenando os arquivos")
    # Concatenar os arquivos
    concat_csv_files(files)
    print("Concatenando o arquivo final")
    # Concatenar o arquivo final
    df = concat_final_csv()
    print("Gravando os arquivos existentes")
    atualiza_controle(existentes(df))
    print("Removendo os arquivos temporários")
    remove_temp_files(transformacao_dir)
    print("Transformação concluída")
