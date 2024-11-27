import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from carregar.executar_carga import executar_carga as carregar_banco
from extrair import extracao_producao
from extrair.extracao import carregar_xpaths, get_logger
from transformar import transf_producao

# Configuração do logger
logger = get_logger("etl_outros.log")
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
    "etl_outros_incremental",
    default_args=default_args,
    description="ETL para extração, transformação e carga mensal de dados",
    schedule_interval="0 3 11 * *",  # Executa no dia 1 de cada mês às 3h
    start_date=days_ago(1),
    catchup=False,
    max_active_tasks=1,
)

# Variáveis e listas
N_MONTHS = 3
lista_extras = [
    "producao_procedimento",
    "producao_procedimentos_odontologicos",
    "producao_aleitamento",
    "producao_vacinacao",
    "producao_acoes",
    "producao_racionalidade",
    "producao_consulta_odontologica",
    "producao_vigilancia_bucal",
    "producao_conduta_odontologica",
    "producao_visita",
    "producao_desfecho_visita",
    "producao_imovel",
    "producao_profissionais_odontologico",
    "producao_profissionais_procedimentos",
    "producao_profissionais_visita",
]


# Funções Python
def limpa_diretorios():
    """Limpa diretórios de download e transformação."""
    down_dir = os.getenv("DOWNLOAD_DIR", "data/download")
    transf_dir = os.getenv("TRANSFORM_DIR", "data/transformacao")
    logger.info(" -- Limpando diretórios -- ")
    os.system(f"rm -rf {down_dir}/*")
    os.system(f"rm -rf {transf_dir}/*")


def executar_extracao(lista=None):
    """Executa a extração baseada no tipo e na lista de arquivos."""
    for producao in lista:
        extracao_producao.executar_downloads_mes(
            xpaths["producao"]["municipio"],
            xpaths[producao]["coluna"],
            xpaths[producao]["checkbox"],
            producao,
            N_MONTHS,
        )


def executar_transformacao():
    """Executa transformações nos dados extraídos."""
    transf_producao.main()


def executar_carga(tipo):
    """Carrega os dados transformados no banco."""
    logger.info(f" -- Realizando carga para o tipo: {tipo} -- ")
    # Implementar lógica de carga no banco de dados aqui.
    carregar_banco(tipo)


dummy_task = PythonOperator(
    task_id="dummy_task",
    python_callable=lambda: None,
    dag=dag,
)

previous_task = dummy_task
# Tasks por grupo de dados do site
for item in lista_extras:
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
