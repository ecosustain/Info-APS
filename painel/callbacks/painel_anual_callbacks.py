import dash.dependencies as dd
import plotly.graph_objects as go
from paginas.painel_anual import colunas, df


def filter_data(municipio, ano, grupo):
    """Função para filtrar os dados do DataFrame"""
    colunas_selecionadas = colunas[grupo]
    return df[(df["Municipio"] == municipio) & (df["Ano"] == ano)][
        colunas_selecionadas + ["Data"]
    ]


def register_callbacks(app):
    """Função para registrar os callbacks"""

    @app.callback(
        [
            dd.Output("grafico-evolucao-problemas", "figure"),
            dd.Output("grafico-problemas-resumo", "figure"),
        ],
        [
            dd.Input("dropdown-grupo", "value"),
            dd.Input("dropdown-municipio", "value"),
            dd.Input("slider-ano", "value"),
        ],
    )
    def update_graphs(grupo, municipio, ano):
        df_filtrado = filter_data(municipio, ano, grupo)

        # Gráfico de barras empilhadas para evolução dos problemas
        fig_evolucao = go.Figure()
        colunas_selecionadas = colunas[grupo]

        for problema in colunas_selecionadas:
            fig_evolucao.add_trace(
                go.Bar(
                    x=df_filtrado["Data"],
                    y=df_filtrado[problema],
                    name=problema,
                    hovertemplate="%{y} casos",
                )
            )
        fig_evolucao.update_layout(
            barmode="stack", title=f"Evolução {grupo} ao Longo do Ano"
        )

        # Gráfico de barras horizontal para problemas totais no período
        problemas_totais = df_filtrado[colunas_selecionadas].sum()
        fig_resumo = go.Figure()
        fig_resumo.add_trace(
            go.Bar(
                y=problemas_totais.index,
                x=problemas_totais.values,
                orientation="h",
            )
        )
        fig_resumo.update_layout(
            title=f"{grupo} Totais no Ano",
            xaxis_title="Total de Atendimentos",
            yaxis_title="Atendimentos de Saúde",
        )

        return fig_evolucao, fig_resumo
