# Previsão de Dados de Saúde Básica
Módulo de previsão de dados de saúde básica utilizando modelos de machine learning.

## Objetivo

Capturar os dados de saúde básica disponíveis na base dados e prever os valores futuros com base em modelos de machine learning.

## Metodologia

- Após finalização do ETL, atualizar os modelos e prever os valores futuros com base nos dados disponíveis.

- Avaliar os últimos 3 meses disponíveis e extrair a combinação de categoria, grupo e municipio.

- Para cada registro de combinação extrair os dados dos últimos X meses.

    - Treinar o modelo com os dados disponíveis e prever os valores futuros.
    - Apagar os registros antigos e inserir os novos registros previstos.
