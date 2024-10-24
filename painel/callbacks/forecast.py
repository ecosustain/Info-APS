"""Módulo para gerar previsões com SARIMA"""

import pandas as pd
from callbacks.data_processing import trimestre_map_num
from statsmodels.tsa.statespace.sarimax import SARIMAX


def preprocess_sarima_data(df):
    df_grouped_mes = (
        df.groupby(
            ["ano_trimestre", "ano", "trimestre", "mes"], observed=True
        )["valor"]
        .sum()
        .reset_index()
        .sort_values(["ano", "mes"])
    )
    df_grouped_mes.reset_index(drop=True, inplace=True)
    return df_grouped_mes[:-1]  # Desconsiderar o último mês


def fit_sarima_model(df_sarima):
    model = SARIMAX(
        df_sarima["valor"], order=(2, 0, 3), seasonal_order=(1, 1, 2, 12)
    )
    results = model.fit(disp=False)
    return results.get_forecast(steps=6)


def generate_forecast_dates(df_sarima):
    """Função para gerar os trimestres para os quais a previsão será feita."""
    last_year = df_sarima["ano"].max()
    last_month = df_sarima[df_sarima["ano"] == last_year]["mes"].max()

    forecast_month = []
    forecast_year = []
    for i in range(1, 7):
        if last_month == 12:
            last_month = 1
            last_year += 1
        else:
            last_month += 1
        forecast_month.append(last_month)
        forecast_year.append(last_year)

    forecast_trimestre = [trimestre_map_num[m] for m in forecast_month]
    forecast_index = [
        f"{t}/{y}" for t, y in zip(forecast_trimestre, forecast_year)
    ]
    return forecast_index


def create_forecast_df(forecast_index, forecast_values):
    """Função para criar o dataframe com a previsão."""
    forecast_df = pd.DataFrame(
        {"ano_trimestre": forecast_index, "valor": forecast_values}
    )
    forecast_df = (
        forecast_df.groupby("ano_trimestre")["valor"].sum().reset_index()
    )
    forecast_df["valor"] = forecast_df["valor"].astype(str)
    return forecast_df


def forecast_sarima(df):
    """Função para gerar a previsão com SARIMA."""
    df_sarima = preprocess_sarima_data(df)
    forecast = fit_sarima_model(df_sarima)
    forecast_index = generate_forecast_dates(df_sarima)
    forecast_values = forecast.predicted_mean
    return create_forecast_df(forecast_index, forecast_values)
