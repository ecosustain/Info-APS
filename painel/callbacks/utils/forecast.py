"""Módulo para gerar previsões com SARIMA"""

import pandas as pd
from callbacks.utils.data_processing import trimestre_map_num
from statsmodels.tsa.statespace.sarimax import SARIMAX


def preprocess_sarima_data(df):
    """Função para pré-processar os dados para o modelo SARIMA."""
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


def fit_sarima_model(df_sarima, steps):
    """Função para treinar o modelo SARIMA."""
    model = SARIMAX(
        df_sarima["valor"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)
    )
    results = model.fit(disp=False)
    return results.get_forecast(steps=steps)


def get_n_months(last_month):
    """Função para obter o número de meses para a previsão."""
    resto = last_month % 3
    if resto == 0:
        return 6
    elif resto == 1:
        return 7
    else:
        return 8


def get_last_month(df_sarima):
    """Função para obter o último mês do dataframe."""
    last_year = df_sarima["ano"].max()
    last_month = df_sarima[df_sarima["ano"] == last_year]["mes"].max()
    return last_month


def generate_forecast_dates(df_sarima):
    """Função para gerar os trimestres para os quais a previsão será feita."""
    last_year = df_sarima["ano"].max()
    last_month = df_sarima[df_sarima["ano"] == last_year]["mes"].max()
    n = get_n_months(last_month)

    forecast_month = []
    forecast_year = []
    for i in range(1, n):
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

    # Criar colunas auxiliares para o ano e o trimestre
    forecast_df["ano"] = forecast_df["ano_trimestre"].apply(
        lambda x: int(x.split("/")[1])
    )
    forecast_df["trimestre"] = forecast_df["ano_trimestre"].apply(
        lambda x: int(x.split("/")[0][1])
    )

    # Ordenar os dados com base nas colunas auxiliares
    forecast_df = forecast_df.sort_values(by=["ano", "trimestre"])

    # Remover as colunas auxiliares
    forecast_df = forecast_df.drop(columns=["ano", "trimestre"])

    forecast_df["valor"] = forecast_df["valor"].astype(str)
    return forecast_df


def ajusta_forecast(df, steps):
    """Função para ajustar o forecast para o número de trimestres."""
    if steps == 7:
        df = df.iloc[1:]
    return df


def forecast_sarima(df):
    """Função para gerar a previsão com SARIMA."""
    df_sarima = preprocess_sarima_data(df)
    steps = get_n_months(get_last_month(df_sarima)) - 1
    forecast = fit_sarima_model(df_sarima, steps)
    forecast_index = generate_forecast_dates(df_sarima)
    forecast_values = forecast.predicted_mean
    forecast_df = create_forecast_df(forecast_index, forecast_values)
    forecast_df = ajusta_forecast(forecast_df, steps)
    return forecast_df
