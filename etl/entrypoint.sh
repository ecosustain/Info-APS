#!/bin/bash
set -e

# Inicializa o banco de dados se necessário
if [[ "$1" == "webserver" ]]; then
    echo "Inicializando o banco de dados..."
    airflow db migrate
    airflow connections create-default-connections
    airflow users create \
        --username admin \
        --password admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com || true
    echo "Banco de dados inicializado."
    airflow scheduler &
    echo "Scheduler iniciado."
fi

# Executa o comando especificado
exec airflow "$@"
