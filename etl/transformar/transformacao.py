"""Módulo para transformação dos dados."""

import os
import shutil

import pandas as pd

# Carregar as configurações
transformacao_dir = os.getenv("TRANSFORMACAO_DIR", "data/transformacao")


def process_csv(file_path, file_type="producao"):
    """
    Função para processar o arquivo CSV e retornar um DataFrame.
    O parâmetro file_type determina se o arquivo é de produção ou cadastro.
    """
    try:
        if file_type == "producao":
            # Processamento específico para o arquivo de produção
            temp_df = pd.read_csv(
                file_path, nrows=10, header=None, encoding="ISO-8859-1"
            )
            linha = temp_df.iloc[3].dropna().values[0]  # Linha 4 (index 3)
            mes, ano = extract_mes_ano_producao(linha)

            df = pd.read_csv(
                file_path, skiprows=7, encoding="ISO-8859-1", sep=";"
            )
            df = df[:-2]  # Remover as 2 últimas linhas

        else:
            # Processamento específico para o arquivo de cadastro
            df = pd.read_csv(
                file_path, skiprows=7, encoding="ISO-8859-1", sep=";"
            )
            df = df[:-3]  # Remover as 3 últimas linhas
            df = df.iloc[:, :-1]  # Remover a última coluna
            mes, ano = extract_mes_ano_cadastro(df)
            # Renomear e preencher a última coluna para mes
            df.rename(columns={df.columns[-1]: "Cadastros"}, inplace=True)
            # renomear a coluna IBGE para Ibge
            df.rename(columns={"IBGE": "Ibge"}, inplace=True)

        # Adicionar as colunas de mês e ano
        df["Mes"] = mes
        df["Ano"] = ano

        # Conversão de tipos (float para int, se houver)
        df = convert_float_to_int(df)

    except Exception as e:
        print(f"Erro ao processar o arquivo {file_type}: {file_path}", e)
        # Incluir no log
        raise e

    return df


def extract_mes_ano_producao(linha):
    """Extrair o mês e o ano do arquivo de produção"""
    mes = linha.split(" ")[1].split("/")[0]
    ano = linha.split(" ")[1].split("/")[1]
    return mes, ano


def extract_mes_ano_cadastro(df):
    """Extrair o mês e o ano do arquivo de cadastro"""
    coluna = df.columns[-1]
    mes = coluna.split("/")[0]
    ano = coluna.split("/")[1][:4]
    return mes, ano


def convert_float_to_int(df):
    """Converter colunas de float para int"""
    for col in df.select_dtypes(include=["float64"]).columns:
        df[col] = df[col].astype(int)
    return df


def concat_csv_files(files, file_type="producao"):
    """Função para concatenar os arquivos CSV em grupos de 100"""
    df = pd.DataFrame()
    colunas = process_csv(files[0], file_type).columns.tolist()

    for i, file in enumerate(files):
        try:
            temp_df = process_csv(file, file_type)
        except Exception as e:
            print(f"ERRO {file_type}: ", file, e)
            continue

        if temp_df.columns.tolist() != colunas:
            print(f"{file} não possui as colunas esperadas")
            continue

        df = pd.concat([df, temp_df])

        if i % 100 == 0 and i > 0:
            df.to_csv(f"partial_{i}_{file_type}.csv", index=False)
            df = pd.DataFrame()

    df.to_csv(f"partial_{i}_{file_type}.csv", index=False)


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


def concat_final_csv(name, diretorio="."):
    """Função para concatenar os arquivos CSV"""
    # Inicializar um DataFrame vazio
    df = pd.DataFrame()
    for file in list_files(diretorio):
        df_temp = pd.read_csv(file)
        df = pd.concat([df, df_temp])
    # Remove duplicados
    df.drop_duplicates(inplace=True)
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


def main(file_type="producao"):
    """Função principal"""
    print("Iniciando a transformação dos dados")
    # Listar os arquivos
    files = list_files(transformacao_dir)
    # Pegar a posicao da ultima barra do primeiro arquivo
    p = files[0].rfind("_")
    # Pega o nome do arquivo sem a data
    nome_arq = files[0][:p]
    print("Concatenando os arquivos")
    # Concatenar os arquivos
    concat_csv_files(files, file_type)
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
