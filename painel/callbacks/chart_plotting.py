"""Módulo para gerar gráficos interativos com Plotly Express"""

import plotly.express as px
import plotly.graph_objects as go
from callbacks.forecast import forecast_sarima

type_color_map = {
    "brasil": ["#B36CA3", "#632956", "#3B032F"],
    "estado": ["#80B0DC", "#34679A", "#11173F"],
    "regiao": ["#97C471", "#2B7B6F", "#11302B"],
    "municipio": ["#FFC20D", "#F7941C", "#A7620E"],
}


def update_layout_chart(chart, title, tipo):
    """Para atualizar o layout do gráfico
    chart -> o gráfico que vamos alterar
    title -> string com o nome que deve aparecer no label do gráfico
    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    retorna o gráfico atualizado"""

    color = type_color_map.get(tipo, [None])[1]

    chart.update_traces(
        textposition="outside",
        marker_color=color,
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#343A40", font_size=12),
        hovertemplate=f"<b>%{{y:,.0f}}</b><br>{title} em %{{x}}<extra></extra>",
    )

    chart.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="#FFFFFF",
        yaxis=dict(showticklabels=False, range=[0, chart.data[0].y.max()*1.1]),
        margin=dict(l=35, r=35, t=60, b=40),
    )

    return chart


def update_layout_chart_profissionais(chart, title, tipo):
    """Para atualizar o layout do gráfico
    chart -> o gráfico que vamos alterar
    title -> string com o nome que deve aparecer no label do gráfico
    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    retorna o gráfico atualizado"""

    # color1 = type_color_map.get(tipo, [None])[0]
    # color2 = type_color_map.get(tipo, [None])[1]

    # Aplicar as duas cores alternadamente
    chart.update_traces(
        textposition="outside",
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#343A40", font_size=12),
        hovertemplate=f"<b>%{{y:,.0f}}</b><br>{title} por %{{fullData.name}} em %{{x}}<extra></extra>",
    )

    chart.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend_title=None,
        plot_bgcolor="#FFFFFF",
        yaxis=dict(showticklabels=False, range=[0, (chart.data[0].y.max()+chart.data[1].y.max()) * 1.1]),
        margin=dict(l=35, r=35, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.95,
        ),  # , xanchor="center", x=0.5 )
    )

    return chart


def get_chart_by_year_profissionais(df, title, tipo):
    """Retorna o gráfico de barras com o total acumulado dos últimos 6 anos de dados
    df -> dados para gerar o gráfico que deve conter ['ano', 'valor']
    title -> string com o nome que deve aparecer no label do gráfico
    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    retorna o gráfico gerado."""

    # Agrupar os dados por ano e quarter somando os valores
    df = df[
        (df["profissional"] == "medico") | (df["profissional"] == "enfermeiro")
    ]
    df_grouped = (
        df.groupby(["profissional", "ano"], observed=True)["valor"]
        .sum()
        .reset_index()
    )
    df_grouped = df_grouped.sort_values("ano")
    df_filtered = df_grouped.tail(6 * df_grouped["profissional"].nunique())

    color1 = type_color_map.get(tipo, [None])[0]
    color2 = type_color_map.get(tipo, [None])[1]

    # Criar gráfico de barras empilhadas
    chart = px.bar(
        df_filtered,
        x="ano",
        y="valor",
        color="profissional",  # Agrupar por profissional
        text_auto=".2s",
        title=f"{title.capitalize()} por Ano",
        labels={
            "ano": "Ano",
            "valor": "Valor",
            "profissional": "Profissional",
        },
        color_discrete_map={  # Mapear cores específicas para cada profissional
            "medico": color1,
            "enfermeiro": color2,
        },
    )

    # Atualizar para o layout padrão
    chart = update_layout_chart_profissionais(chart, title, tipo)

    return chart


def get_chart_by_year(df, title, tipo):
    """Retorna o gráfico de barras com o total acumulado dos últimos 6 anos de dados
    #    df -> dados para gerar o gráfico que deve conter ['ano', 'valor']
    #    title -> string com o nome que deve aparecer no label do gráfico
    #    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    # retorna o gráfico gerado."""

    # Agrupar os dados por ano e quarter somando os valores
    df_grouped = (
        df.groupby(["ano"], observed=True)["valor"].sum().reset_index()
    )
    df_grouped = df_grouped.sort_values("ano")
    df_filtered = df_grouped.tail(6)

    # Criar gráfico de barras
    chart = px.bar(
        df_filtered,
        x="ano",
        y="valor",
        text_auto=".2s",
        title=f"{title.capitalize()} por Ano",
    )

    # Atualizar para o layout padrão
    chart = update_layout_chart(chart, title, tipo)

    return chart


def get_chart_percentage_by_year(df, title, tipo):
    """Retorna o gráfico de barras com o percentual entre os dois valores acumulado dos últimos 6 anos de dados
    #    df -> dados para gerar o gráfico que deve conter ['ano', 'valor1', 'valor2']
    #    title -> string com o nome que deve aparecer no label do gráfico
    #    type -> string para saber em qual agregação estamos ['brasil', 'estado', 'regiao_saude', 'municipio']
    # retorna o gráfico gerado."""

    # Gera as porcentagens antes de gerar o gráfico
    df_grouped = (
        df.groupby("ano", observed=True).apply(lambda x: (x["valor_1"].sum() / x["valor_2"].sum())*100).reset_index(name="valor")
    )

    return get_chart_by_year(df_grouped, title, tipo)


def preprocess_data(df):
    """Pré-processamento dos dados para gerar o modelo de previsão."""
    df_grouped = (
        df.groupby(["ano_trimestre", "ano", "trimestre"], observed=True)[
            "valor"
        ]
        .sum()
        .reset_index()
    )
    df_grouped["ano_order"] = df_grouped["ano"].astype(str) + df_grouped[
        "trimestre"
    ].astype(str).str.replace("T", "")
    df_grouped = df_grouped.sort_values("ano_order")
    return df_grouped.tail(20)


def create_bar_chart(df_filtered, title, tipo):
    """Função para criar o gráfico de barras."""
    chart = px.bar(
        df_filtered,
        x="ano_trimestre",
        y="valor",
        text_auto=".2s",
        title=f"{title.capitalize()} por Trimestre",
    )
    chart = update_layout_chart(chart, title, tipo)
    return chart


def add_forecast_to_chart(chart, forecast_df, tipo):
    """Função para adicionar a previsão ao gráfico."""
    chart.add_trace(
        go.Scatter(
            x=forecast_df["ano_trimestre"],
            y=forecast_df["valor"],
            mode="lines+markers+text",
            text=[f"{y:.3s}" for y in forecast_df["valor"]],
            textposition="top center",
            name="Previsão",
            line=dict(
                color=type_color_map.get(tipo, [None])[1], width=2, dash="dash"
            ),
            hovertemplate="<b>%{{y:,.0f}}</b><br>Previsão para o %{{x}}<extra></extra>",
            hoverlabel=dict(
                bgcolor="#FFFFFF", font_color="#343A40", font_size=12
            ),
        )
    )
    return chart


def get_chart_by_quarter(df, title, tipo):
    """Função para gerar o gráfico de barras com a previsão."""
    df_filtered = preprocess_data(df)
    chart = create_bar_chart(df_filtered, title, tipo)
    forecast_df = forecast_sarima(df)
    chart = add_forecast_to_chart(chart, forecast_df, tipo)
    return chart
