from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from extrair import (
    extracao_cadastros,
    extracao_codigos,
    extracao_gravidas,
    extracao_producao,
)
from extrair.extracao import carregar_xpaths, get_logger
from transformar import transf_producao, transformacao
from carregar.executar_carga import executar_carga as carregar_banco
import os

# Configuração do logger
logger = get_logger("etl.log")
xpaths = carregar_xpaths()

# Configuração inicial da DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["alert@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "etl_producao",
    default_args=default_args,
    description="ETL para extração, transformação e carga mensal de dados",
    schedule_interval="0 3 1 * *",  # Executa no dia 1 de cada mês às 3h
    start_date=days_ago(1),
    catchup=False,
    max_active_tasks=1,
)

# Variáveis e listas
N_MONTHS = 3
lista_site = [
    "producao_profissionais_individual",
    "producao_conduta",
    "producao_condicao",
    "producao_tipo",
]


# Funções Python
def limpa_diretorios():
    """Limpa diretórios de download e transformação."""
    down_dir = os.getenv("DOWNLOAD_DIR", "data/download")
    transf_dir = os.getenv("TRANSFORM_DIR", "data/transformacao")
    logger.info(" -- Limpando diretórios -- ")
    os.system(f"rm -rf {down_dir}/*")
    os.system(f"rm -rf {transf_dir}/*")


def executar_extracao(tipo, lista=None):
    """Executa a extração baseada no tipo e na lista de arquivos."""
    if tipo == "cadastros":
        extracao_cadastros.download_cadastro(N_MONTHS)
    elif tipo == "codigos":
        extracao_codigos.extrair_codigos(N_MONTHS)
    elif tipo == "gravidas":
        extracao_gravidas.executar_downloads_mes(
            xpaths["gravidas"]["municipio"],
            xpaths["gravidas"]["coluna"],
            "gravidas",
            N_MONTHS,
        )
    elif tipo == "lista":
        for producao in lista:
            extracao_producao.executar_downloads_mes(
                xpaths["producao"]["municipio"],
                xpaths[producao]["coluna"],
                xpaths[producao]["checkbox"],
                producao,
                N_MONTHS,
            )
    else:
        raise ValueError(f"Tipo de extração não reconhecido: {tipo}")


def executar_transformacao(tipo):
    """Executa transformações nos dados extraídos."""
    if tipo == "cadastro":
        transformacao.main("cadastro")
    else:
        transf_producao.main()

def executar_carga(tipo):
    """Carrega os dados transformados no banco."""
    logger.info(f" -- Realizando carga para o tipo: {tipo} -- ")
    # Implementar lógica de carga no banco de dados aqui.
    carregar_banco(tipo)

# Cadastros
limpar_cadastros = PythonOperator(
    task_id="limpar_diretorios_cadastros",
    python_callable=limpa_diretorios,
    dag=dag,
)

extrair_cadastros = PythonOperator(
    task_id="extrair_cadastros",
    python_callable=executar_extracao,
    op_kwargs={"tipo": "cadastros"},
    dag=dag,
)

transformar_cadastros = PythonOperator(
    task_id="transformar_cadastros",
    python_callable=executar_transformacao,
    op_kwargs={"tipo": "cadastro"},
    dag=dag,
)

carregar_cadastros = PythonOperator(
    task_id="carregar_cadastros",
    python_callable=executar_carga,
    op_kwargs={"tipo": "cadastro"},
    dag=dag,
)

# Codigos
limpar_codigos = PythonOperator(
    task_id="limpar_diretorios_codigos",
    python_callable=limpa_diretorios,
    dag=dag,
)

extrair_codigos = PythonOperator(
    task_id="extrair_codigos",
    python_callable=executar_extracao,
    op_kwargs={"tipo": "codigos"},
    dag=dag,
)

transformar_codigos = PythonOperator(
    task_id="transformar_codigos",
    python_callable=executar_transformacao,
    op_kwargs={"tipo": "codigos"},
    dag=dag,
)

carregar_codigos = PythonOperator(
    task_id="carregar_codigos",
    python_callable=executar_carga,
    op_kwargs={"tipo": "codigos"},
    dag=dag,
)

# Gravidas
limpar_gravidas = PythonOperator(
    task_id="limpar_diretorios_gravidas",
    python_callable=limpa_diretorios,
    dag=dag,
)

extrair_gravidas = PythonOperator(
    task_id="extrair_gravidas",
    python_callable=executar_extracao,
    op_kwargs={"tipo": "gravidas"},
    dag=dag,
)

transformar_gravidas = PythonOperator(
    task_id="transformar_gravidas",
    python_callable=executar_transformacao,
    op_kwargs={"tipo": "gravidas"},
    dag=dag,
)

carregar_gravidas = PythonOperator(
    task_id="carregar_gravidas",
    python_callable=executar_carga,
    op_kwargs={"tipo": "gravidas"},
    dag=dag,
)

# Definir dependências para cadastros, códigos e grávidas
(
    limpar_cadastros >> extrair_cadastros >> transformar_cadastros >> carregar_cadastros
    >> limpar_codigos >> extrair_codigos >> transformar_codigos >> carregar_codigos
    >> limpar_gravidas >> extrair_gravidas >> transformar_gravidas >> carregar_gravidas
)


# Tasks por grupo de dados do site
previous_task = carregar_gravidas
for item in lista_site:
    limpar = PythonOperator(
        task_id=f"limpar_diretorios_{item}",
        python_callable=limpa_diretorios,
        dag=dag,
    )

    extrair = PythonOperator(
        task_id=f"extrair_{item}",
        python_callable=executar_extracao,
        op_kwargs={"tipo": "lista", "lista": [item]},
        dag=dag,
    )

    transformar = PythonOperator(
        task_id=f"transformar_{item}",
        python_callable=executar_transformacao,
        op_kwargs={"tipo": item},
        dag=dag,
    )

    carregar = PythonOperator(
        task_id=f"carregar_{item}",
        python_callable=executar_carga,
        op_kwargs={"tipo": item},
        dag=dag,
    )

    # Definir dependências
    previous_task >> limpar >> extrair >> transformar >> carregar
    previous_task = carregar
