import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Exemplo de uma série temporal

# Gerar um índice de datas, com o último dia de cada mês, dos últimos 2 anos
data_range = pd.date_range(end=pd.Timestamp.today(), periods=24, freq="M")
# Gerar valores aleatórios para os meses
valores = np.random.randint(100, 1000, size=len(data_range))
# Criar o DataFrame
df = pd.DataFrame({"data": data_range, "valores": valores})

serie_temporal = df["valores"]

result = adfuller(serie_temporal)
print("ADF Statistic:", result[0])
print("p-value:", result[1])

# Ajustar modelo ARIMA(1,1,1) como exemplo
model = ARIMA(serie_temporal, order=(1, 1, 1))
model_fit = model.fit()

# Resumo do modelo
print(model_fit.summary())

# Previsão de 10 períodos à frente
previsoes = model_fit.forecast(steps=10)
print(previsoes)

# Plotar as previsões junto com os dados reais
plt.plot(serie_temporal, label="Dados Reais")
plt.plot(previsoes, label="Previsão", color="red")
plt.legend()
plt.show()
