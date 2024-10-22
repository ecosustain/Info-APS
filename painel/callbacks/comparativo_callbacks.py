"""Módulo com os callbacks da página Comparativa"""

import dash.dependencies as dd
import pandas as pd
import plotly.graph_objects as go
from funcoes import df_norm_uf, df_normalizado, get_columns


def register_callbacks(app):
    """Função para registrar os callbacks"""

    @app.callback(
        [
            dd.Output("tabela-comparativa", "figure"),
            dd.Output("grafico-comparativo-total", "figure"),
            dd.Output("grafico-comparativo-porcentagem", "figure"),
        ],
        [
            dd.Input("dropdown-grupo", "value"),
            dd.Input("dropdown-municipio", "value"),
            dd.Input("slider-ano", "value"),
        ],
    )
    def update_graphs(grupo, municipio, ano):
        """Função para atualizar os gráficos e a tabela"""
        colunas = get_columns()
        cols = colunas[grupo]

        data_inicio = f"{ano}-01-01"
        data_fim = f"{ano}-12-31"

        uf = df_normalizado[df_normalizado["Municipio"] == municipio][
            "Uf"
        ].unique()[0]
        # municipio_nome = municipio
        municipio = (
            df_normalizado[df_normalizado["Municipio"] == municipio]["Ibge"]
            .unique()[0]
            .astype(int)
        )

        df_agp_mu = (
            df_normalizado[
                (df_normalizado["Data"] >= data_inicio)
                & (df_normalizado["Data"] <= data_fim)
            ]
            .groupby("Ibge")
            .sum()
            .reset_index()
            .drop(columns=["Data", "Uf", "populacao"])
        )
        df_agp_uf = (
            df_norm_uf[
                (df_norm_uf["Data"] >= data_inicio)
                & (df_norm_uf["Data"] <= data_fim)
            ]
            .groupby("Uf")
            .sum()
            .reset_index()
            .drop(columns=["Data", "populacao_estado"])
        )

        # Comparar um municipio com o estado em números de atendimento
        df_comp = (
            df_agp_mu[df_agp_mu["Ibge"] == municipio]
            .drop(columns=["Ibge", "Municipio"])
            .reset_index()
            - df_agp_uf[df_agp_uf["Uf"] == uf]
            .drop(columns=["Uf"])
            .reset_index()
        )
        df_comp.drop(columns=["index"], inplace=True)

        # apresentar os dados em um gráfico de barras
        grafico_comparativo_totais = go.Figure()
        # Adicionar as barras
        grafico_comparativo_totais.add_trace(
            go.Bar(
                x=df_comp[cols].values[0],  # Inverter x e y
                y=df_comp[cols].columns,
                name="Diferença",
                orientation="h",  # Definir a orientação como horizontal
            )
        )
        # Configurar o layout do gráfico
        grafico_comparativo_totais.update_layout(
            title="Diferença de atendimentos totais com o Estado",
            xaxis_title="Diferença",
            yaxis_title="Problema",
        )

        # Comparar um municipio com o estado em porcentagem de atendimento
        df_comp_perc = (
            df_agp_mu[df_agp_mu["Ibge"] == municipio]
            .drop(columns=["Ibge", "Municipio"])
            .reset_index()
            / df_agp_uf[df_agp_uf["Uf"] == uf]
            .drop(columns=["Uf"])
            .reset_index()
            * 100
            - 100
        )
        df_comp_perc.drop(columns=["index"], inplace=True)

        # Apresentar os dados em um gráfico de barras horizontal
        grafico_comparativo_porcentagens = go.Figure()
        # Adicionar as barras
        grafico_comparativo_porcentagens.add_trace(
            go.Bar(
                x=df_comp_perc[cols].values[0],  # Inverter x e y
                y=df_comp_perc[cols].columns,
                name="Diferença",
                orientation="h",  # Definir a orientação como horizontal
            )
        )
        # Configurar o layout do gráfico
        grafico_comparativo_porcentagens.update_layout(
            title="Diferença de '%' de atendimentos com o Estado",
            xaxis_title="Diferença (%)",  # Ajuste no título do eixo x
            yaxis_title="Problema",
        )

        # Cria tabela comparativa
        tabela = pd.DataFrame(
            {
                "Problemas": df_comp[cols].columns,
                "Atd Municipio": df_agp_mu[df_agp_mu["Ibge"] == municipio][
                    cols
                ]
                .iloc[0]
                .values,
                "Atd Estado": df_agp_uf[df_agp_uf["Uf"] == uf][cols]
                .iloc[0]
                .values,
                "Dif Atend": df_comp[cols].iloc[0].values,
                "Dif % Atend": df_comp_perc[cols].iloc[0].values,
            }
        ).round(2)

        # Criar a tabela com Plotly
        tabela_comparativa = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(tabela.columns),
                        fill_color="paleturquoise",
                        align="left",
                        font=dict(
                            color="black",
                            size=14,
                            family="Arial",
                            weight="bold",
                        ),
                    ),
                    cells=dict(
                        values=[
                            tabela[col].tolist() for col in tabela.columns
                        ],
                        fill_color="lavender",
                        align="left",
                        font=dict(color="black", size=12, family="Arial"),
                    ),
                )
            ]
        )

        tabela_comparativa.update_layout(
            title="Tabela Comparativa", title_x=0.5
        )

        return (
            tabela_comparativa,
            grafico_comparativo_totais,
            grafico_comparativo_porcentagens,
        )
