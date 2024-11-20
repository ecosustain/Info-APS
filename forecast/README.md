# Previsão de Dados de Saúde Básica
Módulo de previsão de dados de saúde básica utilizando modelos de machine learning.

## Objetivo

Capturar os dados de saúde básica disponíveis na base dados e prever os valores futuros com base em modelos de machine learning.

## Metodologia

Analisadas diferentes estratégias para treinamento de modelos, onde verificou-se que o uso de modelos locais para a previsão das séries temporais apresentou um melhor desemepenho.
Foi utilizado o modelo SARIMA para a previsão dos dados de saúde básica, que é um modelo de séries temporais que leva em consideração a sazonalidade e a tendência dos dados.

O modelo foi otimizado e os resultados foram avaliados com base em métricas de erro, como a raiz quadrada do erro médio (RMSE). Os melhores hiperparametros obtidos foram utilizados para a previsão dos dados futuros. 

### `order (2, 0, 3)`

Este parâmetro representa a parte **não sazonal** do modelo SARIMA, especificando o comportamento do modelo ARIMA "clássico" (sem sazonalidade). Ele é composto de três valores, representados como `(p, d, q)`:

- **p = 2**: Ordem do termo **AR (Auto-Regressivo)**. Indica que o modelo considera os dois períodos anteriores para prever o valor atual.
- **d = 0**: Termo de **diferença**. Neste caso, `d = 0` indica que não há diferenciação aplicada, ou seja, a série original já é considerada estacionária.
- **q = 3**: Ordem do termo **MA (Média Móvel)**. Indica que o modelo considera os resíduos de até três períodos anteriores para ajustar a previsão atual.

### `seasonal_order (1, 1, 2, 12)`

Este parâmetro representa a parte **sazonal** do modelo SARIMA e é composto por quatro valores, representados como `(P, D, Q, s)`:

- **P = 1**: Ordem sazonal do termo **AR (Auto-Regressivo)**. Indica que o modelo considera a dependência sazonal de um período anterior em cada ciclo sazonal completo.
- **D = 1**: Termo de **diferença sazonal**. Indica que uma diferenciação sazonal é aplicada à série para tornar os ciclos sazonais estacionários.
- **Q = 2**: Ordem sazonal do termo **MA (Média Móvel)**. Indica que o modelo considera os resíduos de até dois períodos sazonais anteriores para ajustar a previsão.
- **s = 12**: **Período sazonal**. Um valor de 12 indica sazonalidade anual em dados mensais (ou seja, o ciclo se repete a cada 12 meses).

### Resumo do Modelo SARIMA(2, 0, 3)(1, 1, 2, 12)

Esse modelo SARIMA possui uma estrutura de dependência com dois componentes principais:
- Componente **não sazonal** `(2, 0, 3)`
- Componente **sazonal** `(1, 1, 2, 12)`


O modelo considera a dependência de dois períodos anteriores para prever o valor atual, bem como a dependência sazonal de um período anterior em cada ciclo sazonal completo. Além disso, ele ajusta a previsão com base nos resíduos de até três períodos anteriores (não sazonais) e dois períodos sazonais anteriores.