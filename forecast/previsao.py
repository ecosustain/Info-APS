"""Módulo para gerar as previsões de Produção do SISAB."""

from statsmodels.tsa.statespace.sarimax import SARIMAX


def previsao_sarima(
    dados, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), steps=6
):
    """Gera a previsão de Produção utilizando SARIMA."""
    model = SARIMAX(dados, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit(disp=False)
    forecast = model_fit.forecast(steps)

    return forecast
