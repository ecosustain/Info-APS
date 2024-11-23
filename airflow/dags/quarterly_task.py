from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define a função da tarefa
def hello_world():
    print(f"Hello, World! Task executed at {datetime.now()}")

# Define o DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'quarterly_hello_world',
    default_args=default_args,
    description='A simple quarterly task',
    schedule_interval='0 0 1 */3 *',  # Primeiro dia de cada trimestre
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    task = PythonOperator(
        task_id='hello_world_task',
        python_callable=hello_world,
    )