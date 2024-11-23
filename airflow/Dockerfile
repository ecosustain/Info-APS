# Usa a imagem oficial do Airflow como base
FROM apache/airflow:2.7.1-python3.10

# Instala dependências adicionais (se necessário)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Define o diretório de trabalho no Airflow
WORKDIR /opt/airflow

# Inicialize o banco de dados e crie conexões padrão no entrypoint
ENTRYPOINT ["/bin/bash", "-c", "\
    airflow db migrate && \
    airflow connections create-default-connections && \
    exec airflow webserver & airflow scheduler"]